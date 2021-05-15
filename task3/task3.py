import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from pathlib import Path
import csv
from typing import NoReturn


def extract_from_vector(feature_names, items) -> list[list]:

    score_vals = []
    feature_vals = []

    for idx, score in items:
        score_vals.append(score)
        feature_vals.append(feature_names[idx])

    results = []
    for idx in range(len(feature_vals)):
        results.append([feature_vals[idx], score_vals[idx]])

    return results


def pre_process(text: str) -> str:
    text = text.lower()
    return text


def learn(filepath: Path):
    documentA = pd.read_csv(filepath, delimiter='\n', names=['text'])
    documentA['text'] = documentA['text'].apply(lambda x: pre_process(x))
    docs = documentA['text'].tolist()
    cv = CountVectorizer()
    word_count = cv.fit_transform(docs)
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(word_count)
    return tfidf_transformer, cv


def read_documents(docs: list[Path]) -> list:
    documents = []
    for doc in docs:
        with open(doc, 'r', encoding='utf-8') as f:
            document = f.read()
        document = pre_process(document)
        documents.append(document)

    return documents


def process(filepath: list[Path], tfidf_transformer: TfidfTransformer, cv: CountVectorizer) -> list[list]:
    documents = read_documents(filepath)
    feature_names = cv.get_feature_names()

    tf_idf_vector = tfidf_transformer.transform(cv.transform(documents))
    coo_matrix = tf_idf_vector.tocoo()
    items = zip(coo_matrix.col, coo_matrix.data)
    keywords = extract_from_vector(feature_names, items)
    return keywords


def save_to_csv(data: list[list], filename: Path) -> NoReturn:
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        for row in data:
            csv_writer.writerow(row)


if __name__ == "__main__":
    _learn = Path('files/x_learn.txt')
    _test = Path('files/x_test.txt')
    _result_file = Path('files/result.csv')
    docs = [_learn, _test]
    tfidf, cv = learn(_learn)
    keywords = process(docs, tfidf, cv)
    save_to_csv(keywords, _result_file)
