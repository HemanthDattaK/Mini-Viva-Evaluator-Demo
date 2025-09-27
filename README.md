
# 📝 Mini Viva Evaluator Demo

A web-based application that evaluates short text answers against a reference answer using Hugging Face NLP models. It provides a score (0–5), feedback, and similarity percentage based on semantic similarity and key concept coverage.

---

## 🎯 Objective

* **Input:** Short text answer (typed; no audio support yet)
* **Logic:** Use NLP embeddings to evaluate student answers against reference answers
* **Output:**

  * **Score:** 0–5
  * **Feedback:** Short textual feedback explaining the score
  * **Similarity:** Percentage similarity

---

## 💻 Features

* Semantic similarity scoring using `sentence-transformers`
* Coverage of key concepts
* Completeness check
* Accuracy / Correctness hints
* Brevity vs. detail consideration
* Simple, clean web interface

---

## ⚙️ Setup Instructions

1️⃣ **Clone the repository**

```bash
git clone https://github.com/HemanthDattaK/Mini-Viva-Evaluator-Demo
cd mini-viva-evaluator
```

2️⃣ **Create a virtual environment (recommended)**

```bash
python -m venv venv
```

3️⃣ **Activate the virtual environment**

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux / macOS:**

```bash
source venv/bin/activate
```

4️⃣ **Install required packages**

```bash
pip install -r requirements.txt
```

> ⚠️ Installing `torch` and `sentence-transformers` may take a few minutes depending on your internet speed.

5️⃣ **Set Hugging Face token**

> Important: To run the project, you need a Hugging Face token. Do **not** hardcode your token.

* Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
* Create a new token with **Read** role
* Set it as an environment variable:

```bash
# Windows
set HF_API_TOKEN=<your_token_here>

# Linux/macOS
export HF_API_TOKEN=<your_token_here>
```

Or create a `.env` file in the project root:

```
HF_API_TOKEN=<your_token_here>
```

6️⃣ **Run the application**

```bash
python app.py
```

7️⃣ **Open in browser**
Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see the Mini Viva Evaluator interface.

---

## 🗂 File Structure

```
mini-viva-evaluator/
│
├─ app.py             # Main Flask app
├─ evaluator.py       # NLP evaluation pipeline (uses HF token from env)
├─ templates/
│   └─ index.html     # Web interface template
├─ static/
│   └─ style.css      # Custom styles
├─ requirements.txt   # Python dependencies
└─ README.md          # Project documentation
```

---

## 🧰 Technologies Used

* Python 3.x
* Flask – Web framework
* Hugging Face / sentence-transformers – NLP embeddings
* NumPy & Scikit-learn – Similarity computation

---

## 📝 Usage

1. Open the web page
2. Enter **Reference Answer** (optional, can leave blank)
3. Enter **Student Answer**
4. Click **Submit**
5. View **Score**, **Feedback**, and **Similarity** below

