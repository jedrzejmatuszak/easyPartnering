import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

with open('files/x_learn.txt', 'r', encoding='utf-8') as file:
    dataset = file.readlines()

tfIdfVectorizer=TfidfVectorizer(use_idf=True)
tfIdf = tfIdfVectorizer.fit_transform(dataset)
df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)
print(df.head(25))
