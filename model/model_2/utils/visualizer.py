import torch
import spacy
from transformers import AutoTokenizer
from sklearn.preprocessing import LabelEncoder

import model_2.data_type.enum as data_type
from model_2.model.model import BertForSequenceClassification

class Visualizer:
    def __init__(
        self, 
        nlp=spacy.load("fr_core_news_sm"),
        tokenizer=AutoTokenizer.from_pretrained("dbmdz/bert-base-french-europeana-cased", clean_up_tokenization_spaces=True
    )):
        self.tokenizer = tokenizer
        self.nlp = nlp

    def __make_inference(self, model, label_encoder, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt")

        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        output = label_encoder.inverse_transform(torch.max(outputs, 1).indices)
        return output[0]

    
    def __IOB_tagging(self, sentence):
        le_iob = LabelEncoder()
        le_iob.fit(data_type.IOBTypes._member_names_)

        model = BertForSequenceClassification(len(le_iob.classes_))
        model.load("NER_model.pth")

        sentence = f"END {sentence.lower()} END"
        doc_sentence = self.nlp(sentence)
        tagged_sentence = ""

        for idx, word in enumerate([token_word.text for token_word in doc_sentence]):
            sub_sentence = doc_sentence[idx].text

            if(idx + 1 > 1):
                sub_sentence = f"{sub_sentence}[{status}] "
                tagged_sentence += f"{sub_sentence}"

            for word in doc_sentence[idx + 1 : idx + 7]:
                word_to_add = word.text
                if(word.text == "."):
                    word_to_add = "None"
                sub_sentence = f"{sub_sentence} {word_to_add}"

            status = self.__make_inference(model, le_iob, sub_sentence)

        individual_words = tagged_sentence.split()

        names = []
        for idx, word in enumerate(individual_words):
            status = word[-3:]
            trimmed_word = word[:-3]
            if(status == "[B]"):
                names.append(trimmed_word)

            if(status == "[I]"):
                if(trimmed_word == "."):
                    continue
                names[len(names) - 1] = f"{names[len(names) - 1]} {trimmed_word}"

        return names


    def __get_status_preds(self, sentence, cities):
        le_statuses = LabelEncoder()
        le_statuses.fit(data_type.CityType._member_names_)

        model = BertForSequenceClassification(len(le_statuses.classes_))
        model.load("model.pth")

        response = []

        sentence = sentence.lower()
        for city in cities:
            sentence = sentence.replace(city, f"[[{city}]]")

            output = self.__make_inference(model, le_statuses, sentence)

            sentence = sentence.replace(f"[[{city}]]", city)
            response.append(
                {
                    "status": output,
                    "city": city
                }
            )

        return response 

    def pipeline(self, sentence):
        cities = self.__IOB_tagging(sentence)
        status_preds = self.__get_status_preds(sentence, cities)
        return status_preds
