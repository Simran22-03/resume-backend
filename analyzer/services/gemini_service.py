import os
import json

from dotenv import load_dotenv
from google import genai


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Gemini API Key
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found. Please check your .env file."
    )


# ==========================================================
# Gemini Client
# ==========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)



# ==========================================================
# Resume Analyzer
# ==========================================================

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Your task is to compare a resume with a job description
like a professional ATS system.

Analyze ONLY:

- Programming languages
- Frameworks
- Libraries
- Databases
- Cloud technologies
- DevOps tools
- AI/ML tools
- Certifications
- Technical requirements


RULES:

1. Extract technical skills from the job description.

2. Extract technical skills from the resume.

3. Compare both.

4. missing_skills must contain ONLY skills:
   - present in job description
   - missing from resume


5. Use exact skill names.

GOOD:

[
"React.js",
"Docker",
"AWS",
"PostgreSQL",
"FastAPI"
]


BAD:

[
"Programming",
"Technology",
"Development",
"Communication"
]


6. strengths should only contain things supported by the resume.

7. suggestions should improve ATS score.


Do not invent information.

Return ONLY valid JSON.

Resume:

{resume_text}


Job Description:

{job_description}


Return this format:

{{
    "ats_score": 0,
    "resume_match": 0,

    "missing_skills": [],

    "strengths": [],

    "suggestions": []
}}
"""


    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )


        text = response.text.strip()


        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


        return json.loads(text)


    except Exception as e:

        print("Analyzer Error:", e)


        return {

            "ats_score": 0,

            "resume_match": 0,

            "missing_skills": [],

            "strengths": [],

            "suggestions": [],

            "error": str(e)

        }



# ==========================================================
# AI Resume Chatbot
# ==========================================================

def ask_chatbot(question, analysis):


    prompt = f"""
You are ResumeAI, a friendly AI Resume Assistant.


Your job is to help users understand their resume analysis.


Resume Analysis:

{json.dumps(analysis, indent=4)}



User Question:

{question}



Instructions:

- Reply naturally like a human assistant.
- If user says hi/hello, greet them normally.
- Be friendly and professional.
- Do not behave like an ATS scanner.
- Explain answers clearly.
- Use bullet points when explaining multiple things.
- Keep answers easy to understand.
- Only use information available in the analysis.
- Do not invent resume details.
-Do not summarize resume until and unless asked by user.


Example:

User:
Hi


Assistant:

Hi! 👋

I'm your ResumeAI assistant.

I can help you understand your ATS score, missing skills, strengths, and ways to improve your resume.

How can I help you today?


"""


    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash",

            contents=prompt,

        )


        return {

            "answer": response.text.strip()

        }



    except Exception as e:


        print("Chatbot Error:", e)


        return {

            "answer": "Sorry, I couldn't answer your question.",

            "error": str(e)

        }