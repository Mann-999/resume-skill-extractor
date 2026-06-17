from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfplumber
from google import genai
import os
import tempfile
import json
import re

from extractor import extract_skills
from predict import analyze_resume, predict_roles
from report import generate_report

app = Flask(__name__)
CORS(app)

gemini_client = genai.Client(api_key="AIzaSyCPJwv9MdC639lN9DZVuORLU-Oaob3no_M")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = []
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=1, y_tolerance=3)
            pages.append(text or "")
        return "\n".join(pages)


# ── /upload ──────────────────────────────────────────────────────────────────

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files supported"}), 400

    text = extract_text_from_pdf(file)
    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"}), 400

    result = analyze_resume(text)
    result["raw_text"] = text
    return jsonify(result)


# ── /rewrite-bullets ─────────────────────────────────────────────────────────

@app.route("/rewrite-bullets", methods=["POST"])
def rewrite_bullets():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        bullets = data.get("bullets", [])

        if not bullets:
            return jsonify({"error": "No bullets provided"}), 400

        bullet_list = "\n".join(f"- {b}" for b in bullets)

        prompt = f"""
You are a professional resume coach.

Rewrite each bullet point to be more impactful, action-oriented, and ATS-friendly.

Return ONLY valid JSON.

Format:
[
  {{
    "original": "...",
    "rewritten": "...",
    "tip": "..."
  }}
]

Bullets:
{bullet_list}
"""

        print("Calling Gemini...")

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("Gemini responded")

        raw = response.text.strip()

        raw = re.sub(
            r"^```json\s*|^```\s*|```$",
            "",
            raw,
            flags=re.MULTILINE
        ).strip()

        print("RAW RESPONSE:")
        print(raw)

        rewrites = json.loads(raw)

        return jsonify({"rewrites": rewrites})

    except Exception as e:
        print("ERROR IN /rewrite-bullets:")
        print(str(e))

        return jsonify({
            "error": str(e)
        }), 500
# ── /match-jds ───────────────────────────────────────────────────────────────

@app.route("/match-jds", methods=["POST"])
def match_jds():
    data = request.get_json()
    resume_text = data.get("resume_text", "")
    jds = data.get("job_descriptions", [])  # list of {title, description}

    if not resume_text or not jds:
        return jsonify({"error": "resume_text and job_descriptions required"}), 400

    jd_block = "\n\n".join(
        f"JD {i+1} - {jd.get('title', f'Job {i+1}')}:\n{jd.get('description', '')}"
        for i, jd in enumerate(jds)
    )

    prompt = f"""You are an expert ATS and resume screener. Analyze the resume against each job description and return a ranked match report.

Return ONLY a JSON array sorted by match_score descending, no markdown, no explanation. Each object must have:
- "title": job title
- "match_score": integer 0-100
- "matched_skills": list of skills from resume that match the JD
- "missing_skills": list of important skills in JD that are missing from resume
- "verdict": one sentence summary

Resume:
{resume_text[:3000]}

Job Descriptions:
{jd_block}"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw = response.text.strip()
    raw = re.sub(r"^```json\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()

    try:
        matches = json.loads(raw)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse Gemini response", "raw": raw}), 500

    return jsonify({"matches": matches})


# ── /generate-report ─────────────────────────────────────────────────────────

@app.route("/generate-report", methods=["POST"])
def generate_report_endpoint():
    data = request.get_json()

    skills = data.get("skills", {})
    predicted_roles = data.get("predicted_roles", [])
    summary = data.get("summary", "")
    reasoning = data.get("reasoning", "")

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    generate_report(skills, predicted_roles, summary, reasoning, output_path)

    return send_file(
        output_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume_report.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)