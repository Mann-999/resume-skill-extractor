import json
import re

with open('skills.json', 'r') as f:
    SKILLS = json.load(f)

def extract_skills(text):
    text_lower = text.lower()
    found = {"technical": [], "soft": []}

    for category, skills in SKILLS.items():
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found[category].append(skill)

    return found

if __name__ == "__main__":
    sample = """
    Experienced software engineer with strong python and machine learning skills.
    Worked with react and nodejs. Good leadership and communication skills.
    Used docker and aws for deployment. Familiar with sql and mongodb.
    """
    result = extract_skills(sample)
    print("Technical skills:", result["technical"])
    print("Soft skills:", result["soft"])