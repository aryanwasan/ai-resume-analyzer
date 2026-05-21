import string
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ai_analysis(resume_text, job_text):
    prompt = f"""
    Analyze this resume against this job description.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_text}
    
    Give me:
    1. Match percentage estimate
    2. Key strengths
    3. Missing skills
    4. One sentence recommendation
    """
    response = client.models.generate_content(
        model="models/gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text

def read_file(filepath):
    with open(filepath,'r') as f:
        return f.read()

def count_words(text):
    words = text.split()
    return len(words)

def count_unique_words(text):
    words = text.lower().split()
    unique = set(words)
    return len(unique)

def extract_keywords(text, keywords):
    words = text.lower().split()
    words = [word.strip(string.punctuation) for word in words]
    found = []
    for word in words:
        if word in keywords:
            found.append(word)
    return found

def match_score(resume_text, job_text, keywords):
    resume_found = extract_keywords(resume_text,keywords)
    job_found = extract_keywords(job_text,keywords)

    matched = set()
    missing = set()

    for keyword in job_found:
        if keyword in resume_found:
            matched.add(keyword)
        else:
            missing.add(keyword)

    score = (len(matched) / len(job_found)) * 100

    return matched, missing, score

resume_path = input("Enter resume file path: ")
job_path = input("Enter job file path: ")
keywords_path = input("Enter keyword file path: ")

resume = read_file(resume_path)
job = read_file(job_path)
keywords = [k.strip() for k in read_file(keywords_path).split(",")]

matched, missing, score = match_score(resume, job, keywords)
print("Matched:", matched)
print("Missing:", missing)
print("Score",round(score,2),"%")

print("\n--- AI Analysis ---")
print(ai_analysis(resume, job))