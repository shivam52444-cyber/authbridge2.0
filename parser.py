# parser.py

import json
import re


def extract_json_block(text: str):
    """
    Extract JSON object from messy LLM output
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def parse_llm_output(output: str):
    try:
        if not output:
            print("❌ Empty LLM output")
            return None, None

        print("\n==============================")
        print("🔴 RAW LLM OUTPUT:\n", output)

        # Remove markdown if present
        cleaned = re.sub(r"```json|```", "", output).strip()

        # Extract JSON block
        json_text = extract_json_block(cleaned)

        if not json_text:
            print("❌ No JSON found")
            return None, None

        print("\n🟢 EXTRACTED JSON:\n", json_text)

        data = json.loads(json_text)

        score = data.get("overall_score", None)

        if score is None:
            print("❌ Missing overall_score")
            return None, None

        # convert to float safely
        score = float(score)

        # normalize if needed
        if score <= 10:
            score = score * 10

        print(f"\n✅ FINAL SCORE: {score}")

        return score, data

    except Exception as e:
        print("❌ PARSE ERROR:", e)
        return None, None