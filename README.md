# AI Resume Skill Extractor

An NLP + ML system that extracts skills from resumes and predicts suitable job roles.

## Tech Stack

- **Backend**: Python, Flask, spaCy, scikit-learn
- **Frontend**: React (Vite)
- **ML**: TF-IDF + classification model

## Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Project Status

- [x] Day 1 — Project setup, virtual env, dependencies installed
- [x] Day 2 — Text preprocessing pipeline, cleaned dataset generated
- [x] Day 3 — Skill ontology built, NLP-based skill extractor working
- [x] Day 4 — ML model trained (Random Forest, 74% accuracy), predict pipeline and parser complete