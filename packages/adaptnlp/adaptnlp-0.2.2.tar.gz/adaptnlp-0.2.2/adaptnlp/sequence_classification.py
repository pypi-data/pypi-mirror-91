import logging
from typing import List, Dict, Union, Tuple, Callable
from collections import defaultdict
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
import datasets
from datasets import ClassLabel
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from flair.data import Sentence, DataPoint
from flair.models import TextClassifier
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    PreTrainedTokenizer,
    PreTrainedModel,
    BertPreTrainedModel,
    DistilBertPreTrainedModel,
    XLMPreTrainedModel,
    XLNetPreTrainedModel,
    ElectraPreTrainedModel,
    BertForSequenceClassification,
    XLNetForSequenceClassification,
    AlbertForSequenceClassification,
    TrainingArguments,
    Trainer,
)

from tqdm import tqdm


from adaptnlp.model import AdaptiveModel

logger = logging.getLogger(__name__)


class TransformersSequenceClassifier(AdaptiveModel):
    """Adaptive model for Transformer's Sequence Classification Model

    Usage:
    ```python
    >>> classifier = TransformersSequenceClassifier.load("transformers-sc-model")
    >>> classifier.predict(text="Example text", mini_batch_size=32)
    ```

    **Parameters:**

    * **tokenizer** - A tokenizer object from Huggingface's transformers (TODO)and tokenizers
    * **model** - A transformers Sequence Classsifciation model
    """

    def __init__(self, tokenizer: PreTrainedTokenizer, model: PreTrainedModel):
        # Load up model and tokenizer
        self.tokenizer = tokenizer
        self.model = model

        # Load empty trainer
        self.trainer = None

        # Setup cuda and automatic allocation of model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    @classmethod
    def load(cls, model_name_or_path: str) -> AdaptiveModel:
        """Class method for loading and constructing this classifier

        * **model_name_or_path** - A key string of one of Transformer's pre-trained Sequence Classifier Model
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)
        classifier = cls(tokenizer, model)
        return classifier

    def predict(
        self,
        text: Union[List[Sentence], Sentence, List[str], str],
        mini_batch_size: int = 32,
        **kwargs,
    ) -> List[Sentence]:
        """Predict method for running inference using the pre-trained sequence classifier model

        * **text** - String, list of strings, sentences, or list of sentences to run inference on
        * **mini_batch_size** - Mini batch size
        * **&ast;&ast;kwargs**(Optional) - Optional arguments for the Transformers classifier
        """
        id2label = self.model.config.id2label
        sentences = text
        results: List[Sentence] = []

        with torch.no_grad():
            if not sentences:
                return sentences

            if isinstance(sentences, DataPoint) or isinstance(sentences, str):
                sentences = [sentences]

            # filter empty sentences
            if isinstance(sentences[0], Sentence):
                sentences = [sentence for sentence in sentences if len(sentence) > 0]
            if len(sentences) == 0:
                return sentences

            # reverse sort all sequences by their length
            rev_order_len_index = sorted(
                range(len(sentences)), key=lambda k: len(sentences[k]), reverse=True
            )
            original_order_index = sorted(
                range(len(rev_order_len_index)), key=lambda k: rev_order_len_index[k]
            )

            reordered_sentences: List[Union[DataPoint, str]] = [
                sentences[index] for index in rev_order_len_index
            ]
            # Turn all Sentence objects into strings
            if isinstance(reordered_sentences[0], Sentence):
                str_reordered_sentences = [
                    sentence.to_original_text() for sentence in sentences
                ]
            else:
                str_reordered_sentences = reordered_sentences

            # Tokenize and get dataset
            dataset = self._tokenize(str_reordered_sentences)
            dataloader = DataLoader(dataset, batch_size=mini_batch_size)
            predictions: List[Tuple[str, float]] = []

            logger.info(f"Running prediction on {len(dataset)} text sequences")
            logger.info(f"Batch size = {mini_batch_size}")
            for batch in tqdm(dataloader, desc="Predicting text"):
                self.model.eval()
                batch = tuple(t.to(self.device) for t in batch)

                if len(batch) == 3:
                    inputs = {
                        "input_ids": batch[0],
                        "attention_mask": batch[1],
                        "token_type_ids": batch[2],
                    }
                else:
                    inputs = {"input_ids": batch[0], "attention_mask": batch[1]}
                outputs = self.model(**inputs)
                logits = outputs[0]
                preds = torch.softmax(logits, dim=1).tolist()

                predictions += preds

            for text, pred in zip(str_reordered_sentences, predictions):
                # Initialize and assign labels to each class in each datapoint prediction
                text_sent = Sentence(text)
                for k, v in id2label.items():
                    text_sent.add_label(label_type="sc", value=v, score=pred[k])
                results.append(text_sent)

        # Order results back into original order
        results = [results[index] for index in original_order_index]

        return results

    def _tokenize(
        self, sentences: Union[List[Sentence], Sentence, List[str], str]
    ) -> TensorDataset:
        """ Batch tokenizes text and produces a `TensorDataset` with them """

        # TODO: __call__ from tokenizer base class in the transformers library could automate/handle this
        tokenized_text = self.tokenizer.batch_encode_plus(
            sentences,
            return_tensors="pt",
            pad_to_max_length=True,
            add_special_tokens=True,
        )

        # Bart, XLM, DistilBERT, RoBERTa, and XLM-RoBERTa don't use token_type_ids
        if isinstance(
            self.model,
            (
                BertForSequenceClassification,
                XLNetForSequenceClassification,
                AlbertForSequenceClassification,
            ),
        ):
            dataset = TensorDataset(
                tokenized_text["input_ids"],
                tokenized_text["attention_mask"],
                tokenized_text["token_type_ids"],
            )
        else:
            dataset = TensorDataset(
                tokenized_text["input_ids"], tokenized_text["attention_mask"]
            )

        return dataset

    def train(
        self,
        training_args: TrainingArguments,
        train_dataset: datasets.Dataset,
        eval_dataset: datasets.Dataset,
        text_col_nm: str = "text",
        label_col_nm: str = "label",
        compute_metrics: Callable = None,
    ) -> None:
        """Trains and/or finetunes the sequence classification model

        * **training_args** - Transformers `TrainingArguments` object model
        * **train_dataset** - Training `Dataset` class object from the datasets library
        * **eval_dataset** - Eval `Dataset` class object from the datasets library
        * **text_col_nm** - Name of the text feature column used as training data (Default "text")
        * **label_col_nm** - Name of the label feature column (Default "label")
        * **compute_metrics** - Custom metrics function callable for `transformers.Trainer`'s compute metrics
        * **return** - None
        """
        # Set default metrics if None
        if not compute_metrics:
            compute_metrics = self._default_metrics

        # Set datasets.Dataset label values in sequence classifier configuration
        ## Important NOTE: Updating configurations do not update the sequence classification head module layer
        ## We are manually initializing a new linear layer for the "new" labels being trained
        class_label = train_dataset.features[label_col_nm]
        config_data = {
            "num_labels": class_label.num_classes,
            "id2label": {v: n for v, n in enumerate(class_label.names)},
            "label2id": {n: v for v, n in enumerate(class_label.names)},
        }
        self.model.config.update(config_data)
        self._mutate_model_head(class_label=class_label)

        # Batch map datasets as torch tensors with tokenizer
        def tokenize(batch):
            return self.tokenizer(batch[text_col_nm], padding=True, truncation=True)

        train_dataset = train_dataset.map(
            tokenize, batch_size=len(train_dataset), batched=True
        )
        eval_dataset = eval_dataset.map(
            tokenize, batch_size=len(eval_dataset), batched=True
        )

        # Rename label col name to match model forward signature of "labels" or ["label","label_ids"] since these are addressed by the default collator from transformers
        train_dataset.rename_column_(
            original_column_name=label_col_nm, new_column_name="labels"
        )
        eval_dataset.rename_column_(
            original_column_name=label_col_nm, new_column_name="labels"
        )

        # Set format as torch tensors for training
        train_dataset.set_format(
            "torch", columns=["input_ids", "attention_mask", "labels"]
        )
        eval_dataset.set_format(
            "torch", columns=["input_ids", "attention_mask", "labels"]
        )

        # Instantiate transformers trainer
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            compute_metrics=compute_metrics,
        )

        # Train and serialize
        self.trainer.train()
        self.trainer.save_model()
        self.tokenizer.save_pretrained(training_args.output_dir)

    def evaluate(self) -> Dict[str, float]:
        """Evaluates model specified

        * **model_name_or_path** - The model name key or model path
        """
        if not self.trainer:
            logger.info("No trainer loaded, must run `classifier.train(...)` first")
            ValueError("Trainer not found, must run train() method")
        return self.trainer.evaluate()

    def _mutate_model_head(self, class_label: ClassLabel) -> None:
        """Manually intialize new linear layers for prediction heads on specific language models that we're trying to train on"""
        if isinstance(self.model, (BertPreTrainedModel, DistilBertPreTrainedModel)):
            self.model.classifier = nn.Linear(
                self.model.config.hidden_size, class_label.num_classes
            )
            self.model.num_labels = class_label.num_classes
        elif isinstance(self.model, XLMPreTrainedModel):
            self.model.num_labels = class_label.num_classes
        elif isinstance(self.model, XLNetPreTrainedModel):
            self.model.logits_proj = nn.Linear(
                self.model.config.d_model, class_label.num_classes
            )
            self.model.num_labels = class_label.num_classes
        elif isinstance(self.model, ElectraPreTrainedModel):
            self.model.num_labels = class_label.num_classes
        else:
            logger.info(f"Sorry, can not train on a model of type {type(self.model)}")

    # Setup default metrics for sequence classification training
    def _default_metrics(self, pred) -> Dict:
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average=None
        )
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


class FlairSequenceClassifier(AdaptiveModel):
    """Adaptive Model for Flair's Sequence Classifier...very basic

    Usage:
    ```python
    >>> classifier = FlairSequenceClassifier.load("en-sentiment")
    >>> classifier.predict(text="Example text", mini_batch_size=32)
    ```

    **Parameters:**

    * **model_name_or_path** - A key string of one of Flair's pre-trained Sequence Classifier Model
    """

    def __init__(self, model_name_or_path: str):
        self.classifier = TextClassifier.load(model_name_or_path)

    @classmethod
    def load(cls, model_name_or_path: str) -> AdaptiveModel:
        """Class method for loading a constructing this classifier

        * **model_name_or_path** - A key string of one of Flair's pre-trained Sequence Classifier Model
        """
        classifier = cls(model_name_or_path)
        return classifier

    def predict(
        self,
        text: Union[List[Sentence], Sentence, List[str], str],
        mini_batch_size: int = 32,
        **kwargs,
    ) -> List[Sentence]:
        """Predict method for running inference using the pre-trained sequence classifier model

        * **text** - String, list of strings, sentences, or list of sentences to run inference on
        * **mini_batch_size** - Mini batch size
        * **&ast;&ast;kwargs**(Optional) - Optional arguments for the Flair classifier
        """
        if isinstance(text, (Sentence, str)):
            text = [text]
        if isinstance(text[0], str):
            text = [Sentence(s) for s in text]
            
        self.classifier.predict(
            sentences=text,
            mini_batch_size=mini_batch_size,
            **kwargs,
        )


        return text

    def train(self):
        pass

    def evaluate(self):
        pass


class EasySequenceClassifier:
    """Sequence classification models

    Usage:

    ```python
    >>> classifier = EasySequenceClassifier()
    >>> classifier.tag_text(text="text you want to label", model_name_or_path="en-sentiment")
    ```

    """

    def __init__(self):
        self.sequence_classifiers: Dict[AdaptiveModel] = defaultdict(bool)

    def tag_text(
        self,
        text: Union[List[Sentence], Sentence, List[str], str],
        model_name_or_path: str = "en-sentiment",
        mini_batch_size: int = 32,
        **kwargs,
    ) -> List[Sentence]:
        """Tags a text sequence with labels the sequence classification models have been trained on

        * **text** - String, list of strings, `Sentence`, or list of `Sentence`s to be classified
        * **model_name_or_path** - The model name key or model path
        * **mini_batch_size** - The mini batch size for running inference
        * **&ast;&ast;kwargs** - (Optional) Keyword Arguments for Flair's `TextClassifier.predict()` method params
        **return** A list of Flair's `Sentence`'s
        """
        # Load Text Classifier Model and Pytorch Module into tagger dict
        if not self.sequence_classifiers[model_name_or_path]:
            """
            self.sequence_classifiers[model_name_or_path] = TextClassifier.load(
                model_name_or_path
            )
            """
            # TODO: Find an alternative model-check method like an `is_available(model_name_or_path)
            # Check whether this is a Transformers or Flair Sequence Classifier model we're loading
            try:
                self.sequence_classifiers[
                    model_name_or_path
                ] = FlairSequenceClassifier.load(model_name_or_path)
            except (NotADirectoryError, FileNotFoundError, IsADirectoryError):
                logger.info(
                    f"{model_name_or_path} not a valid Flair pre-trained model...checking transformers repo"
                )
                try:
                    self.sequence_classifiers[
                        model_name_or_path
                    ] = TransformersSequenceClassifier.load(model_name_or_path)
                except ValueError:
                    logger.info("Try transformers")
                    return [Sentence("")]

        classifier = self.sequence_classifiers[model_name_or_path]
        return classifier.predict(
            text=text,
            mini_batch_size=mini_batch_size,
            **kwargs,
        )

    def tag_all(
        self,
        text: Union[List[Sentence], Sentence, List[str], str],
        mini_batch_size: int = 32,
        **kwargs,
    ) -> List[Sentence]:
        """Tags text with all labels from all sequence classification models

        * **text** - Text input, it can be a string or any of Flair's `Sentence` input formats
        * **mini_batch_size** - The mini batch size for running inference
        * **&ast;&ast;kwargs** - (Optional) Keyword Arguments for Flair's `TextClassifier.predict()` method params
        * **return** - A list of Flair's `Sentence`'s
        """
        sentences = text
        for tagger_name in self.sequence_classifiers.keys():
            sentences = self.tag_text(
                sentences,
                model_name_or_path=tagger_name,
                mini_batch_size=mini_batch_size,
                **kwargs,
            )
        return sentences

    def train(
        self,
        training_args: TrainingArguments,
        train_dataset: Union[str, Path, datasets.Dataset],
        eval_dataset: Union[str, Path, datasets.Dataset],
        model_name_or_path: str = "bert-base-uncased",
        text_col_nm: str = "text",
        label_col_nm: str = "label",
        label_names: List[str] = None,
    ) -> None:
        """Trains and/or finetunes the sequence classification model

        * **model_name_or_path** - The model name key or model path
        * **training_args** - Transformers `TrainingArguments` object model
        * **train_dataset** - Training `Dataset` class object from the datasets library or path to CSV file (labels must be int values)
        * **eval_dataset** - Eval `Dataset` class object from the datasets library or path to CSV file (labels must be int values)
        * **text_col_nm** - Name of the text feature column used as training data (Default "text")
        * **label_col_nm** - Name of the label feature column (Default "label")
        * **label_names** - (Only when loading CSV) An ordered list of label strings with int label mapped to string via. index value
        * **return** - None
        """

        # Dynamically load sequence classifier
        if not self.sequence_classifiers[model_name_or_path]:
            try:
                self.sequence_classifiers[
                    model_name_or_path
                ] = TransformersSequenceClassifier.load(model_name_or_path)
            except ValueError:
                logger.info("Try transformers model")

        classifier = self.sequence_classifiers[model_name_or_path]

        # Check if csv filepath or `datasets.Dataset`
        if not isinstance(train_dataset, datasets.Dataset):
            train_dataset = self._csv2dataset(
                data_path=train_dataset,
                label_col_nm=label_col_nm,
                label_names=label_names,
            )
        if not isinstance(eval_dataset, datasets.Dataset):
            eval_dataset = self._csv2dataset(
                data_path=eval_dataset,
                label_col_nm=label_col_nm,
                label_names=label_names,
            )

        classifier.train(
            training_args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            text_col_nm=text_col_nm,
            label_col_nm=label_col_nm,
        )

    def release_model(
        self,
        model_name_or_path: str,
    ) -> None:
        """Unload model from classifier and empty cuda mem cache (may leave residual cache per pytorch documentation on torch.cuda.empty_cache())

        * **model_name_or_path** - The model name or key path that you want to unload and release memory from
        """
        if self.sequence_classifiers[model_name_or_path].trainer:
            del self.sequence_classifiers[model_name_or_path].trainer
        del self.sequence_classifiers[model_name_or_path]
        torch.cuda.empty_cache()

    def evaluate(
        self,
        model_name_or_path: str = "bert-base-uncased",
    ) -> Dict[str, float]:
        """Evaluates model specified

        * **model_name_or_path** - The model name key or model path
        """

        # Dynamically load sequence classifier
        if not self.sequence_classifiers[model_name_or_path]:
            try:
                self.sequence_classifiers[
                    model_name_or_path
                ] = TransformersSequenceClassifier.load(model_name_or_path)
            except ValueError:
                logger.info("Try transformers model")

        classifier = self.sequence_classifiers[model_name_or_path]

        return classifier.evaluate()

    def _csv2dataset(
        self,
        data_path: Union[str, Path],
        label_col_nm: str,
        label_names: List[str],
    ) -> datasets.Dataset:
        """Loads CSV path as an datasets.Dataset for downstream use"""
        if not label_names:
            raise ValueError(
                "Must pass in `label_names` parameter for training when loading in CSV datasets."
            )
        class_label = datasets.ClassLabel(
            num_classes=len(label_names), names=label_names
        )
        dataset = datasets.load_dataset("csv", data_files=data_path)
        dataset = dataset["train"]
        dataset.features[label_col_nm] = class_label
        return dataset
