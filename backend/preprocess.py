import pandas as pd
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def preprocess(text):
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha and len(token) > 2
    ]
    return " ".join(tokens)

def load_and_preprocess(filepath):
    df = pd.read_csv(filepath)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nSample:\n", df.head(3))
    print("\nJob categories:\n", df['Category'].value_counts())
    df['cleaned'] = df['Resume_str'].apply(preprocess)
    df.to_csv('data/cleaned_resumes.csv', index=False)
    print("\nDone. Saved to data/cleaned_resumes.csv")
    return df

if __name__ == "__main__":
    load_and_preprocess('./data/Resume.csv')