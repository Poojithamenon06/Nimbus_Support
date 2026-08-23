# Nimbus Support — Tier-1 AI Employee

A support triage assistant that classifies incoming questions, answers them
using retrieval-augmented generation (RAG) over a 28-article knowledge base,
and escalates to a human whenever it isn't confident, stating the reason.

Built for: Supervity FDE Technical Screening — Problem 3 (Customer Support
AI Employee, Tier-1 Triage).

## Tech stack

- **Backend:** Flask (Python)
- **Database:** SQLite (stdlib `sqlite3`, no ORM — easy to read line by line)
- **Retrieval:** scikit-learn TF-IDF + cosine similarity over the knowledge base
- **Generation (optional):** Claude API, grounded strictly in the retrieved article.
  If no API key is set, the app falls back to returning the matched article's
  content directly — it works with zero setup either way.
- **Frontend:** Server-rendered Jinja2 templates + vanilla JS (no build step)

## Why this architecture (design tradeoff)

Retrieval uses TF-IDF rather than a neural embedding model. That's a deliberate
tradeoff: TF-IDF needs no model download, no GPU, and no API key, so the app
works instantly for any reviewer who clones it. The cost is weaker semantic
matching — it won't realize "I can't log in" and "reset my password" are related
unless the words overlap. A production version would swap this for
sentence-transformer or Claude embeddings for better semantic recall, at the
cost of a slower cold start.

## Project structure

```
nimbus-ai-support/
├── app.py                 # Flask routes + API endpoints
├── database.py             # SQLite schema + queries
├── retrieval.py             # TF-IDF classification + retrieval (the "R" in RAG)
├── llm.py                   # Optional Claude-based grounded answer generation
├── requirements.txt
├── .env.example              # copy to .env to add an API key (optional)
├── data/
│   └── kb_seed.py             # 28 knowledge base articles, 4 categories
├── templates/                 # Dashboard, Live Chat, Tickets, Escalations, KB
└── static/
    ├── css/style.css
    └── js/ (chat.js, tickets.js, kb.js)
```

## Setup — from zero

1. Install Python 3.10+ if you don't have it.
2. Open a terminal in this folder.
3. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   pip install -r requirements.txt
   ```
4. (Optional) Copy `.env.example` to `.env` and add an `ANTHROPIC_API_KEY` if
   you want Claude-generated conversational answers instead of raw article text.
5. Run it:
   ```
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

The SQLite database (`nimbus.db`) and the knowledge base seed data are created
automatically on first run — nothing else to configure.

## Assumptions made

- Escalation is triggered by retrieval match confidence (how well the query
  matches *any* knowledge base article), not by classification confidence
  (which category it belongs to) — these measure different things, and only
  the former tells you whether the answer is trustworthy.
- Confidence threshold for escalation defaults to 0.28 (cosine similarity),
  configurable via `.env`. Tuned empirically against the seed KB.
- Mock/synthetic data only — no real customer data used.
- Single-reviewer scope: no authentication layer, since the brief specifies
  mock data and a single evaluator, not multi-tenant production use.
