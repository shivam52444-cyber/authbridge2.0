from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from aiengine import llm 

from langchain_core.prompts import PromptTemplate

jd_prompt = PromptTemplate.from_template("""
Act as a Senior Technical Recruiter and HR Expert with 20 years of experience in talent acquisition. Analyze the following Job Description (JD) provided below and provide a detailed breakdown.

Your analysis must be structured exactly as follows:

### 1. Mandatory Skills (Hard Skills)
- List the essential technical skills, tools, or qualifications required.
- Assign a weight (%) to each based on importance to reach a total of 100% for this section.

### 2. Good-to-Have Skills (Preferred)
- List the skills that are not mandatory but preferred.
- Assign a weight (%) to each based on added value to reach a total of 100% for this section.

### 3. Soft Skills
- List the necessary behavioral traits, communication skills, or cultural fit factors.
- Assign a weight (%) to each based on importance to reach a total of 100% for this section.

### 4. Final Analysis: JD Difficulty Rating
- Analyze the overall requirement. Is this role asking for more skills than usual (over-scoped/\"unicorn\" hunt), less skill than usual (under-scoped), or is it balanced for the role level?
- Provide a brief justification for your conclusion.



Format:

{{
  "must_have_skills": [{{"skill": "", "weight": 0}}],
  "good_to_have_skills": [{{"skill": "", "weight": 0}}],
  "soft_skills": [{{"skill": "", "weight": 0}}],
  "final anlysis": Final analysis
  
}}

Rules:
- Weights must sum to 100
- No explanations
- Keep skills short

Job Description:
{jd}
""")

jd_chain = jd_prompt | llm | StrOutputParser()


def analyze_jd(jd_text):
    return jd_chain.invoke({"jd": jd_text})

