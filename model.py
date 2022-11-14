from transformers import AutoTokenizer, AutoModel
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'


class LanguageModel(object):

    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/sbert_large_mt_nlu_ru")
        enc = AutoModel.from_pretrained("sberbank-ai/sbert_large_mt_nlu_ru")
        self.model = {
            'tokenizer': tokenizer,
            'encoder': enc,
        }

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def __call__(self, sentences):
        encoded_input = self.model['tokenizer'](sentences, padding=True, truncation=True, max_length=24,
                                                return_tensors='pt')
        encoded_input = encoded_input.to(device)
        with torch.no_grad():
            model_output = self.model['encoder'].to(device)(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings

