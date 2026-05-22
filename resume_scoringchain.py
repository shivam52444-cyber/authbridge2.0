# resume_scoringchain.py

from jd_analysis_chain import *
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import time
from resumeparser import extract_text
from parser import parse_llm_output


# 🔥 Strong prompt (forces strict JSON)
resume_prompt = PromptTemplate.from_template("""
You are an expert recruiter.

IMPORTANT:
- Return ONLY valid JSON
- Do NOT add explanation
- Do NOT wrap in markdown

Format EXACTLY:

{{
  "overall_score": number (0-100),
  "strengths": ["point1", "point2"],
  "gaps": ["gap1", "gap2"],
  "summary": "short summary",
  "recommendation": "shortlist" or "reject"
}}

Evaluate strictly based on:
- skill match
- experience relevance
- project alignment

JD:
{jd}

Resume:
{resume}
""")


resume_chain = resume_prompt | llm | StrOutputParser()


# 🔥 Retry-safe scoring
def score_resume(jd, resume, retries=3):
    for attempt in range(retries):
        try:
            output = resume_chain.invoke({
                "jd": jd,
                "resume": resume
            })

            print(f"\n🔍 Attempt {attempt+1} RAW OUTPUT:\n", output)

            return output

        except Exception as e:
            print(f"❌ LLM ERROR (attempt {attempt+1}):", e)
            time.sleep(1)

    return None
  
