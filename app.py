from flask import Flask, render_template, request
from evaluator import AnswerEvaluator

app = Flask(__name__)
evaluator = AnswerEvaluator()

@app.route("/", methods=["GET", "POST"])
def home():
    score = feedback = similarity = None
    student_answer = reference_answer = ""

    if request.method == "POST":
        reference_answer = request.form.get("reference_answer", "").strip()
        student_answer = request.form.get("student_answer", "").strip()

        score, feedback, similarity = evaluator.evaluate(student_answer, reference_answer)

    return render_template(
        "index.html",
        reference_answer=reference_answer,
        student_answer=student_answer,
        score=score,
        feedback=feedback,
        similarity=similarity,
    )

if __name__ == "__main__":
    app.run(debug=False)  # production-ready
