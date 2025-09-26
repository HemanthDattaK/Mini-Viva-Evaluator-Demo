

# 📝 Mini Viva Evaluator Demo

A web-based application that evaluates short text answers against a reference answer using **HuggingFace NLP models**. It provides a **score (0–5)**, **feedback**, and **similarity percentage** based on semantic similarity and key concept coverage.

---

## 🎯 Objective

* Input: Short text answer (typed; no audio support yet)
* Logic: Use NLP embeddings to evaluate student answers against reference answers
* Output:

  * **Score:** 0–5
  * **Feedback:** Short textual feedback explaining the score
  * **Similarity:** Percentage similarity

---

## 💻 Features

* Semantic similarity scoring using `sentence-transformers`
* Coverage of key concepts (Supervised vs. Unsupervised, Labeled vs. Unlabeled, Examples like Classification, Regression, Clustering)
* Completeness check
* Accuracy / Correctness hints
* Brevity vs. detail consideration
* Simple, clean web interface

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/HemanthDattaK/Mini-Viva-Evaluator-Demo
cd mini-viva-evaluator
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment

* **Windows**

```bash
venv\Scripts\activate
```

* **Linux / macOS**

```bash
source venv/bin/activate
```

### 4️⃣ Install required packages

```bash
pip install -r requirements.txt
```

> ⚠️ Installing `torch` and `sentence-transformers` may take a few minutes depending on your internet speed.

### 5️⃣ Run the application

```bash
python mini_viva_local.py
```

### 6️⃣ Open in browser

Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to see the Mini Viva Evaluator interface.

---

## 🗂 File Structure

```
mini-viva-evaluator/
│
├─ mini_viva_local.py      # Main Flask app
├─ evaluator.py            # NLP evaluation pipeline
├─ templates/
│   └─ index.html          # Web interface template
├─ static/
│   └─ style.css           # Custom styles
├─ requirements.txt        # Python dependencies
└─ README.md               # Project documentation
```

---

## 🧰 Technologies Used

* **Python 3.x**
* **Flask** – Web framework
* **HuggingFace / sentence-transformers** – NLP embeddings
* **NumPy & Scikit-learn** – Similarity computation

---

## 📝 Usage

1. Open the web page
2. Enter **Reference Answer** (optional, can leave blank)
3. Enter **Student Answer**
4. Click **Submit**
5. View **Score**, **Feedback**, and **Similarity** below
