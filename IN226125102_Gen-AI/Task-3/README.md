# AI Resume Screening System

An LLM-powered pipeline that evaluates candidate resumes against a job description — extracting skills, running gap analysis, scoring fit, and generating explainable feedback. Built with LangChain LCEL and Groq (LLaMA 3.3 70B).

---

## How It Works

The system runs resumes through a 4-step sequential pipeline:

```
Resume → Extraction → Matching → Scoring → Explanation
```

**Step 1 — Extraction**  
Parses the resume strictly — no hallucination, no assumed skills. Returns a structured JSON profile with name, years of experience, skills, tools, education, and key projects.

**Step 2 — Matching**  
Compares extracted profile against the job description. Identifies matched skills, missing skills, and rates experience/education fit as `strong | partial | weak`.

**Step 3 — Scoring**  
Assigns a 0–100 score using a fixed rubric:

| Category | Max Points |
|---|---|
| Skills match | 40 |
| Experience match | 25 |
| Education match | 15 |
| Tools & MLOps | 20 |

Returns grade (A/B/C/D), recommendation, and a cited explanation.

**Step 4 — Explanation**  
Generates a plain-English summary of the score with specific evidence from the resume.

---

## Tech Stack

- **LangChain** — LCEL chains, PromptTemplate, FewShotPromptTemplate
- **Groq API** — LLaMA 3.3 70B Versatile (fast inference)
- **LangSmith** — optional tracing, tagging, and pipeline debugging
- **Python** — JSON parsing, pipeline orchestration

---

## Setup

```bash
pip install langchain langchain-core langchain-groq langsmith python-dotenv
```

Set your API keys:

```python
os.environ["GROQ_API_KEY"] = "your_groq_api_key"
os.environ["LANGCHAIN_API_KEY"] = "your_langsmith_api_key"   # optional
os.environ["LANGCHAIN_TRACING_V2"] = "true"                  # optional
os.environ["LANGCHAIN_PROJECT"] = "AI-Resume-Screening"      # optional
```

To disable LangSmith tracing:

```python
os.environ["LANGCHAIN_TRACING_V2"] = "false"
```

---

## Sample Results

Three candidate types tested against a Data Scientist JD (Python, ML, Deep Learning, NLP, SQL, TensorFlow, PyTorch, 3+ years):

| Candidate | Skills Match | Experience | Score | Recommendation |
|---|---|---|---|---|
| Strong | Python, ML, DL, NLP, SQL, TF, PyTorch | 4 years | 85–95 | Strongly Recommend |
| Average | Python, ML, SQL | 2 years | 50–70 | Consider |
| Weak | Excel only | Fresher | 0–30 | Reject |

---

## Key Design Decisions

- **Temperature 0.0** for extraction and matching → strict, deterministic output
- **Temperature 0.1–0.2** for scoring and explanation → better reasoning without drift
- **Manual prompt construction** instead of chained PromptTemplate → avoids LCEL parsing issues with nested JSON schemas
- **`parse_json()` utility** → handles markdown fences and malformed LLM responses safely
- **Few-shot prompting** included as a bonus module — guides the model toward consistent score formatting

---

## LangSmith Tracing (Optional)

The `screen_resume_with_tags()` function passes `RunnableConfig` with tags and metadata into each LLM call. Traces appear in the LangSmith dashboard under the project name and can be filtered by candidate type.

---

## Project Structure

```
AI-Resume-Screening-System/
├── AI_Resume_Screening_System_with_Tracing.ipynb
└── README.md
```

---

## Author

**Aadesh Yogi**  
[GitHub](https://github.com/aadeshyogi12) · [LinkedIn](https://linkedin.com/in/aadeshyogi)
