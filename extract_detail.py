from aiengine import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional
from pydantic import BaseModel


# -----------------------------
# 1. Schema
# -----------------------------
class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None


# -----------------------------
# 2. Prompt
# -----------------------------
contact_prompt = PromptTemplate.from_template("""
Extract professional contact information from the text below.

Instructions:
- Return ONLY valid JSON (no explanation, no extra text).
- Include:
  - name
  - email
  - mobile_number
- If any field is missing, return null.
- Remove extra spaces from email and mobile_number.

Example:
Input:
"Hi, I’m Shivam Kumar. You can reach me at shivam123@gmail.com or call me at 9876543210."

Output:
{{
  "name": "Shivam Kumar",
  "email": "shivam123@gmail.com",
  "mobile_number": "9876543210"
}}

Text:
{resume}
""")


# -----------------------------
# 3. Chain
# -----------------------------
parser = JsonOutputParser(pydantic_object=ContactInfo)

chain = contact_prompt | llm | parser


# -----------------------------
# 4. Function (ONLY ENTRY POINT)
# -----------------------------
def extract_contact_info(text: str):
    try:
        result = chain.invoke({"resume": text})
        return result
    except Exception:
        return {
            "name": None,
            "email": None,
            "mobile_number": None
        }