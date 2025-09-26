# evaluator.py
from sentence_transformers import SentenceTransformer, util

class AnswerEvaluator:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def evaluate(self, reference, student):
        if not reference or not student:
            return 0, "Reference or student answer is empty.", {"similarity": 0}

        emb_ref = self.model.encode(reference, convert_to_tensor=True)
        emb_stu = self.model.encode(student, convert_to_tensor=True)

        sim_score = util.pytorch_cos_sim(emb_ref, emb_stu).item()  # 0-1
        similarity_percent = round(sim_score * 100, 2)

        # Score logic 0-5
        if sim_score >= 0.85:
            score = 5
            feedback = "Excellent! Most key points are covered."
        elif sim_score >= 0.7:
            score = 4
            feedback = "Good. Some minor points missing."
        elif sim_score >= 0.55:
            score = 3
            feedback = "Fair. Key ideas are partially covered."
        elif sim_score >= 0.4:
            score = 2
            feedback = "Poor. Many key ideas are missing."
        elif sim_score > 0.2:
            score = 1
            feedback = "Very poor. Only a small idea is mentioned."
        else:
            score = 0
            feedback = "No relevant content found."

        return score, feedback, {"similarity": similarity_percent}
