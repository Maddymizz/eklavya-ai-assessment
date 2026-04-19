from agents.generator import GeneratorAgent, GeneratorOutput
from agents.reviewer import ReviewerAgent, ReviewerOutput
from pydantic import BaseModel
from typing import Optional
import traceback

class PipelineResult(BaseModel):
    generated: GeneratorOutput
    review: ReviewerOutput
    refined: Optional[GeneratorOutput] = None
    refined_review: Optional[ReviewerOutput] = None
    refinement_triggered: bool = False

def run_pipeline(grade: int, topic: str) -> PipelineResult:
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    print(f"[Pipeline] Starting for Grade {grade}, Topic: {topic}")

    # Step 1: Generate
    print("[Pipeline] Running Generator Agent...")
    generated = generator.run(grade, topic)
    print(f"[Pipeline] Generated explanation length: {len(generated.explanation)}")
    print(f"[Pipeline] Generated MCQ count: {len(generated.mcqs)}")

    # Step 2: Review
    print("[Pipeline] Running Reviewer Agent...")
    review = reviewer.run(grade, generated)
    print(f"[Pipeline] Review status: {review.status}")
    print(f"[Pipeline] Review scores: {review.scores}")

    refined = None
    refined_review = None
    refinement_triggered = False

    # Step 3: Refine if failed
    if review.status == "fail" and review.feedback:
        print("[Pipeline] Review failed — running refinement...")
        refinement_triggered = True
        try:
            refined = generator.run(grade, topic, feedback=review.feedback)
            refined_review = reviewer.run(grade, refined)
            print(f"[Pipeline] Refined review status: {refined_review.status}")
        except Exception as e:
            print(f"[Pipeline] Refinement failed: {e}")
            refined = None
            refined_review = None
            refinement_triggered = False

    print("[Pipeline] Complete.")
    return PipelineResult(
        generated=generated,
        review=review,
        refined=refined,
        refined_review=refined_review,
        refinement_triggered=refinement_triggered
    )