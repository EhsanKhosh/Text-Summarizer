from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch
import pandas as pd
from tqdm import tqdm
from textSummarizer.entity import EvaluationConfig 


class ModelEvaluation:
    def __init__(self, config: EvaluationConfig) -> None:
        self.config = config

    
    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]

    def calculate_metrics_on_test_ds(self, dataset, metric, model, tokenizer,
                                     batch_size=16, device='cuda' if torch.cuda.is_available() else 'cpu',
                                     column_text='article',
                                     column_summary='summary'):
        article_batch = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batch = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batch, target_batch), total=len(article_batch)):
            
            inputs = tokenizer(article_batch, max_length=1024, truncation=True,
                               paddings="max_length", return_tensors="pt")
            
            summaries = model.generate(inputs_ids=inputs['inputs_ids'].to(device),
                                       attention_mask=inputs['attention_mask'].to(device),
                                       length_penalty=0.8, num_beams=8, max_length=128)
            

            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                                  clean_up_tokenization_spaces=True)
                                 for s in summaries]

            decoded_summaries = [d.replace("", " ") for d in decoded_summaries] 

            metric.add_batch(predictions=decoded_summaries, references=target_batch)

            return metric.compute()
        
        def evaluate(self):
            device = "cuda" if torch.cuda.is_available() else "cpu"
            tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

            dataset_samsum_pt = load_from_disk(self.config.data_path)

            rouge_names = ['rouge1', 'rouge2', 'rougeL', 'rougeLsum']

            rouge_metric = load_metric('rouge')

            score = self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][:10], rouge_metric,
                                                     model, 2, tokenizer, device)
            
            rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)

            df = pd.DataFrame(rouge_dict, index=['pegasus'] )
            df.to_csv(self.config.metric_filename, index=False)