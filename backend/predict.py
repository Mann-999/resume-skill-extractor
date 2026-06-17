import joblib

from extractor import extract_skills
from preprocess import preprocess

model = joblib.load('model/model.pkl')
tfidf = joblib.load('model/vectorizer.pkl')
le = joblib.load('model/label_encoder.pkl')

ROLE_MAPPING = {}

def clean_role(role):
    return role

def predict_roles(text, top_n=5):  # ← changed from 3 to 5

    cleaned = preprocess(text)

    vec = tfidf.transform([cleaned])

    probabilities = model.predict_proba(vec)[0]

    top_indices = probabilities.argsort()[-top_n:][::-1]

    # ── FIXED: normalize against ALL probs, not just top N ──
    total = probabilities.sum()  # always 1.0, keeps real confidence values

    results = []

    for i in top_indices:

        confidence = (probabilities[i] / total) * 100

        results.append({
            "role": clean_role(le.classes_[i]),
            "confidence": round(confidence, 2)
        })

    return results

def generate_reasoning(skills):

    technical = skills.get("technical", [])

    important = technical[:5]

    if not important:
        return "Prediction based on overall resume content."

    return (
        "Prediction influenced by skills such as: "
        + ", ".join(important)
    )

def generate_summary(skills, roles):

    technical = skills.get("technical", [])

    if technical:
        top_skills = ", ".join(technical[:5])
    else:
        top_skills = "general technical capabilities"

    top_role = roles[0]["role"]

    return (
        f"Candidate shows strong exposure to {top_skills}. "
        f"The profile appears most aligned with {top_role} roles."
    )

def analyze_resume(text):

    skills = extract_skills(text)

    roles = predict_roles(text)

    reasoning = generate_reasoning(skills)

    summary = generate_summary(skills, roles)

    return {
        "skills": skills,
        "predicted_roles": roles,
        "reasoning": reasoning,
        "summary": summary
    }

if __name__ == "__main__":

    sample = """
    Experienced software engineer with 3 years of experience
    in python and machine learning.

    Worked with flask, react and nodejs.

    Strong leadership and communication skills.

    Used docker and aws for deployment.

    Familiar with sql and mongodb.

    Developed deep learning models using tensorflow and keras.
    """

    result = analyze_resume(sample)

    print("\nResume Summary:")
    print(result["summary"])

    print("\nTechnical Skills:")
    print(result["skills"]["technical"])

    print("\nSoft Skills:")
    print(result["skills"]["soft"])

    print("\nPrediction Reasoning:")
    print(result["reasoning"])

    print("\nTop Career Matches:")

    for i, role in enumerate(result["predicted_roles"], start=1):

        print(
            f"{i}. {role['role']} "
            f"({role['confidence']}%)"
        )