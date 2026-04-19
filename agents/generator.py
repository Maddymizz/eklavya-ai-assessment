import json
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class GeneratorOutput(BaseModel):
    explanation: str
    mcqs: List[MCQ]

SYSTEM_PROMPT = """You are an expert educational content creator for school students.
You MUST return ONLY a valid JSON object. No markdown, no code fences, no explanation before or after.
The JSON must match this exact structure:
{
  "explanation": "string with 3-4 paragraphs",
  "mcqs": [
    {"question": "string", "options": ["A) text", "B) text", "C) text", "D) text"], "answer": "A"}
  ]
}"""

def build_prompt(grade: int, topic: str, feedback: Optional[List[str]] = None) -> str:
    prompt = f"""Create educational content for Grade {grade} students on: "{topic}"

REQUIREMENTS:
- explanation: Write 3-4 paragraphs teaching this topic clearly for Grade {grade}. Use real examples. Write proper paragraphs, not bullet points.
- mcqs: Create exactly 4 multiple choice questions. Each must have exactly 4 options as ["A) ...", "B) ...", "C) ...", "D) ..."]. Answer field must be just the letter: A, B, C, or D.
- Every MCQ must test a concept DIRECTLY mentioned in your explanation.
- Content must be factually correct and vocabulary must match Grade {grade}.

Return ONLY the JSON object. Nothing else."""

    if feedback:
        prompt += f"""

CRITICAL - This is a REVISED attempt. Fix ALL of these issues from the previous version:
{chr(10).join(f'  - {f}' for f in feedback)}"""

    return prompt

class GeneratorAgent:
    def run(self, grade: int, topic: str, feedback: Optional[List[str]] = None) -> GeneratorOutput:
        prompt = build_prompt(grade, topic, feedback)
        response = client.chat.completions.create(
            model="grok-3-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if model adds them
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    raw = part
                    break
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]
        data = json.loads(raw)
        return GeneratorOutput(**data)