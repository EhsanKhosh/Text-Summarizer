import os
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import torch
from textSummarizer.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        
    
    def train(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt)
        model.to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

        dataset_samsum = load_from_disk(self.config.data_path)

        training_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            warmup_steps=self.config.warmup_steps,
            weight_decay=self.config.weights_decay,
            logging_steps=self.config.logging_steps,
            evaluation_strategy=self.config.evaluation_strategy,
            eval_steps=self.config.eval_steps,
            save_steps=self.config.save_steps,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps)
        
        trainer = Trainer(
            model=model,
            tokenizer=tokenizer,
            args=training_args,
            data_collator=seq2seq_data_collator,
            train_dataset=dataset_samsum['train'],
            eval_dataset=dataset_samsum['validation'])
        
        trainer.train()

        model.save_pretrained(os.path.join(self.config.root_dir,'pegasus-samsum-model'))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir,'pegasus-samsum-tokenizer'))

    