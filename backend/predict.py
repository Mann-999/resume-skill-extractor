import joblib
import os
from extractor import extract_skills
from preprocess import preprocess

model = joblib.load('model/model.pkl')
tfidf = joblib.load('model/vectorizer.pkl')
le = joblib.load('model/label_encoder.pkl')

def predict_roles(text, top_n=3):
    cleaned = preprocess(text)
    vec = tfidf.transform([cleaned])
    probabilities = model.predict_proba(vec)[0]
    top_indices = probabilities.argsort()[-top_n:][::-1]
    results = []
    for i in top_indices:
        results.append({
            "role": le.classes_[i],
            "confidence": round(float(probabilities[i]) * 100, 2)
        })
    return results

def analyze_resume(text):
    skills = extract_skills(text)
    roles = predict_roles(text)
    return {
        "skills": skills,
        "predicted_roles": roles
    }

if __name__ == "__main__":
    sample = """
    Experienced software engineer with 3 years of experience in python and machine learning.
    Worked with flask, react and nodejs. Strong leadership and communication skills.
    Used docker and aws for deployment. Familiar with sql and mongodb.
    Developed deep learning models using tensorflow and keras.
    """
    result = analyze_resume(sample)
    print("Technical Skills:", result["skills"]["technical"])
    print("Soft Skills:", result["skills"]["soft"])
    print("\nPredicted Roles:")
    for r in result["predicted_roles"]:
        print(f"  {r['role']}: {r['confidence']}%")