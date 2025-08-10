import os
import re
import json
import google.generativeai as genai
from .models import Inconsistency

class AIAnalyzer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _clean_json(self, text: str) -> str:
        """Clean Gemini output so it becomes valid JSON."""
        # Remove triple backticks and language tags like ```json
        if text.startswith("```"):
            text = "\n".join(line for line in text.splitlines() if not line.startswith("```"))

        # Replace Python-style escapes with normal chars
        text = text.replace("\\'", "'")

        # Remove trailing commas inside objects/arrays
        text = re.sub(r",\s*([}\]])", r"\1", text)

        return text.strip()

    def check_consistency(self, slides):
        inconsistencies = []

        for i in range(len(slides)):
            for j in range(i + 1, len(slides)):
                prompt = (
                    f"Compare the following slide texts for contradictions:\n"
                    f"Slide {slides[i].slide_number}: {slides[i].text}\n"
                    f"Slide {slides[j].slide_number}: {slides[j].text}\n"
                    "Respond ONLY with valid JSON in the format: "
                    '{"consistent": bool, "reason": str}'
                )

                response = self.model.generate_content(prompt)
                raw_text = response.text or ""

                try:
                    cleaned = self._clean_json(raw_text)
                    verdict = json.loads(cleaned)

                    if not verdict.get("consistent", True):
                        inconsistencies.append(
                            Inconsistency(
                                id=f"I{i}{j}",
                                type="semantic_conflict",
                                description=verdict.get("reason", "Possible contradiction"),
                                slides=[slides[i].slide_number, slides[j].slide_number],
                                evidence=[slides[i].text, slides[j].text],
                                confidence=0.8
                            )
                        )

                except Exception as e:
                    print(f"⚠️ Could not parse LLM response as JSON: {raw_text}\nError: {e}")
                    # Fallback: store raw reason as an "unparsed" inconsistency
                    inconsistencies.append(
                        Inconsistency(
                            id=f"I{i}{j}_raw",
                            type="unparsed_llm_response",
                            description=f"Raw LLM output: {raw_text}",
                            slides=[slides[i].slide_number, slides[j].slide_number],
                            evidence=[slides[i].text, slides[j].text],
                            confidence=0.3
                        )
                    )

        return inconsistencies
