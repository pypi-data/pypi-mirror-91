# coding=utf-8
# This file uses code from the language modeling examples in the huggingface Transformer's repo

import os
import logging
import math
from typing import Dict, Union
from pathlib import Path

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelWithLMHead,
    TrainingArguments,
    Trainer,
    TextDataset,
    DataCollatorForLanguageModeling,
    # TODO: For XLNet, will be available in Transformers release 3.0.2+
    # DataCollatorForPermutationLanguageModeling,
    LineByLineTextDataset,
)

logger = logging.getLogger(__name__)


class LMFineTuner:
    """
     A Language Model Fine Tuner object you can set language model configurations and then train and evaluate

    Usage:

    ```python
    >>> finetuner = adaptnlp.LMFineTuner()
    >>> finetuner.train()
    ```

    **Parameters:**

    * **model_name_or_path** - The model checkpoint for weights initialization. Leave None if you want to train a model from scratch.
    """

    def __init__(
        self,
        model_name_or_path="bert-base-cased",
    ):

        logger.info(
            "This is the new updated `LMFineTuner` class object for 0.2.0+. If you're looking for `LMFineTuner` from <=0.1.6, you can instantiate it with LMFineTunerManual"
        )
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path, use_fast=True
        )
        # TODO: AutoModelWithLMHead deprecated, update to causal, mask, or seq2seq
        self.model = AutoModelWithLMHead.from_pretrained(model_name_or_path)
        self.trainer = None

        # Setup cuda and automatic allocation of model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train(
        self,
        training_args: TrainingArguments,
        train_file: Union[str, Path],
        eval_file: Union[str, Path],
        line_by_line: bool = False,
        mlm: bool = False,
        mlm_probability: float = 0.15,
        plm_probability: float = 1 / 6,
        max_span_length: int = 5,
        block_size: int = -1,
        overwrite_cache: bool = False,
    ):
        """Train and fine-tune the loaded language model

        * **train_file** - The input training data file (a text file).
        * **eval_file** - An optional input evaluation data file to evaluate the perplexity on (a text file).
        * **line_by_line** - Whether distinct lines of text in the dataset are to be handled as distinct sequences.
        * **mlm** - Train with masked-language modeling loss instead of language modeling.
        * **mlm_probability** - Ratio of tokens to mask for masked language modeling loss
        * **plm_probability** - Ratio of length of a span of masked tokens to surrounding context length for permutation language modeling.
        * **max_span_length** - Maximum length of a span of masked tokens for permutation language modeling.
        * **block_size** - Optional input sequence length after tokenization.
                            The training dataset will be truncated in block of this size for training."
                            `-1` will default to the model max input length for single sentence inputs (take into account special tokens).
        * **overwrite_cache** - Overwrite the cached training and evaluation sets
        """

        # Setup logging
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
        )
        logger.warning(
            f"""Process rank: {training_args.local_rank},
                device: {training_args.device},
                n_gpu: {training_args.n_gpu},
                distributed training: {bool(training_args.local_rank != -1)},
                16-bits training: {training_args.fp16}
            """
        )
        logger.info(f"Training/evaluation parameters: {training_args.to_json_string()}")

        # Check if masked language model or not
        if (
            self.model.config.model_type
            in ["bert", "roberta", "distilbert", "camembert"]
            and not mlm
        ):
            raise ValueError(
                """BERT and RoBERTa-like models do not have LM heads but masked LM heads. They must be run with
                mlm set as True(masked language modeling)."""
            )

        # Check block size for Dataset
        if block_size <= 0:
            block_size = self.tokenizer.max_len
        else:
            block_size = min(block_size, self.tokenizer.max_len)

        # Get datasets
        train_dataset = self._get_dataset(
            file_path=train_file,
            line_by_line=line_by_line,
            block_size=block_size,
            overwrite_cache=overwrite_cache,
        )
        eval_dataset = self._get_dataset(
            file_path=eval_file,
            line_by_line=line_by_line,
            block_size=block_size,
            overwrite_cache=overwrite_cache,
        )
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset

        # Get Collator
        # TODO: DataCollatorForPermutationLanguageModeling not availbe until release 3.0.2+
        if self.model.config.model_type == "xlnet":
            logger.info("Cannot currently finetune XLNet model")
            raise ValueError(
                "Use another language model besides XLNet for LM finetuning"
            )
            """
            data_collator = DataCollatorForPermutationLanguageModeling(
            tokenizer=self.tokenizer,
            plm_probability=plm_probability,
            max_span_length=max_span_length,
            )
            """
        else:
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer, mlm=mlm, mlm_probability=mlm_probability
            )

        # Initialize Trainer
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        # Train and serialize
        self.trainer.train()
        self.trainer.save_model()
        self.tokenizer.save_pretrained(training_args.output_dir)

    def evaluate(self) -> Dict[str, float]:

        if not self.trainer:
            logger.info(
                "No trainer loaded, you should probably run `LMFineTuner.train(...)` first"
            )
            return None
        results = {}

        logger.info("*** Evaluate ***")

        eval_output = self.trainer.evaluate()

        perplexity = math.exp(eval_output["eval_loss"])
        result = {"perplexity": perplexity}

        output_eval_file = os.path.join(
            self.trainer.args.output_dir, "eval_results_lm.txt"
        )

        with open(output_eval_file, "w") as writer:
            logger.info("***** Eval results *****")
            for key in sorted(result.keys()):
                logger.info("  %s = %s", key, str(result[key]))
                writer.write("%s = %s\n" % (key, str(result[key])))
        results.update(result)

        return results

    def _get_dataset(
        self,
        file_path: str,
        line_by_line: bool,
        block_size: int,
        overwrite_cache: bool,
    ) -> Dataset:
        if line_by_line:
            return LineByLineTextDataset(
                tokenizer=self.tokenizer, file_path=file_path, block_size=block_size
            )
        else:
            return TextDataset(
                tokenizer=self.tokenizer,
                file_path=file_path,
                block_size=block_size,
                overwrite_cache=overwrite_cache,
            )
