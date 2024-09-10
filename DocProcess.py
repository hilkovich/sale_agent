import json
import time
import pandas as pd

class DocumentProcessor:
    def __init__(self, embeding_model, file_path):
        self.embeding_model = embeding_model
        self.file_path = file_path
    
    def load_reviews(self):
        data = pd.read_excel(self.file_path)
        return data['Review Text'].tolist()

    def get_doc_embeddings(self, docs):
        doc_embeddings = []
        for i, text in enumerate(docs):
            try:
                embedding = json.loads(self.embeding_model.embed_documents(text))["embedding"]
                doc_embeddings.append(embedding)
                time.sleep(0.5)
                print(f"Успешно обработан отзыв {i}")
            except Exception as e:
                print(f"Ошибка при обработке отзыва {i}: {e}")
        return doc_embeddings
    
    def check_embeddings(self, doc_embeddings):
        for emb in doc_embeddings:
            if not isinstance(emb, list):
                raise ValueError(f"Эмбеддинг должен быть списком чисел, но получен {type(emb)}: {emb}")

    def save_embeddings(self, doc_embeddings, output_file):
        with open(output_file, 'w') as f:
            json.dump(doc_embeddings, f)
        print(f"Эмбеддинги успешно сохранены в {output_file}")

    def load_embeddings(self, input_file):
        with open(input_file, 'r') as f:
            return json.load(f)