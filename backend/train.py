import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train():
    print("Loading dataset...")
    df = pd.read_csv('data/cleaned_resumes.csv')
    df = df.dropna(subset=['cleaned', 'Category'])

    print("Encoding labels...")
    le = LabelEncoder()
    y = le.fit_transform(df['Category'])
    X = df['cleaned']

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Vectorizing text...")

    tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": SVC(probability=True, kernel='linear'),
        "Random Forest": RandomForestClassifier(n_estimators=100)
    }

    best_model = None
    best_score = 0
    best_name = ""

    print("\nTraining and comparing models...")
    for name, model in models.items():
        scores = cross_val_score(model, X_train_vec, y_train, cv=5)
        mean_score = scores.mean()
        print(f"{name}: CV Accuracy = {mean_score:.4f}")
        if mean_score > best_score:
            best_score = mean_score
            best_model = model
            best_name = name

    print(f"\nBest model: {best_name} with CV accuracy {best_score:.4f}")

    print("Training best model on full training set...")
    best_model.fit(X_train_vec, y_train)
    y_pred = best_model.predict(X_test_vec)

    print(f"\nTest Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    os.makedirs('model', exist_ok=True)
    joblib.dump(best_model, 'model/model.pkl')
    joblib.dump(tfidf, 'model/vectorizer.pkl')
    joblib.dump(le, 'model/label_encoder.pkl')
    print("\nModel saved to model/")

if __name__ == "__main__":
    train()