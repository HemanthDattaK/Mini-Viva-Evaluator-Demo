# mini_viva_local.py
from flask import Flask, render_template, request
from evaluator import AnswerEvaluator

app = Flask(__name__)
evaluator = AnswerEvaluator()

@app.route("/", methods=["GET", "POST"])
def home():
    reference_answer = ""
    student_answer = ""
    score = None
    feedback = None
    similarity = None

    if request.method == "POST":
        reference_answer = request.form.get("reference_answer", "")
        student_answer = request.form.get("student_answer", "")

        score, feedback, debug = evaluator.evaluate(reference_answer, student_answer)
        similarity = debug['similarity']

    return render_template(
        "index.html",
        reference_answer=reference_answer,
        student_answer=student_answer,
        score=score,
        feedback=feedback,
        similarity=similarity
    )

if __name__ == "__main__":
    app.run(debug=True)
