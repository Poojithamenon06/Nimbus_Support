import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

import database as db
from retrieval import RetrievalEngine
from llm import generate_answer, explain_flag

app = Flask(__name__)

CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.28))

db.init_db()
engine = RetrievalEngine()


@app.route("/")
def dashboard():
    stats = db.dashboard_stats()
    return render_template("dashboard.html", stats=stats, active="dashboard")


@app.route("/chat")
def chat_page():
    return render_template("chat.html", active="chat")


@app.route("/tickets")
def tickets_page():
    tickets = db.list_tickets()
    return render_template("tickets.html", tickets=tickets, active="tickets")


@app.route("/escalations")
def escalations_page():
    escalations = db.list_escalations()
    return render_template("escalations.html", escalations=escalations, active="escalations")


@app.route("/knowledge-base")
def kb_page():
    articles = db.list_kb_articles()
    by_cat = {}
    for a in articles:
        by_cat.setdefault(a["category"], []).append(a)
    return render_template("knowledge_base.html", by_cat=by_cat, active="kb")


# API 

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "empty message"}), 400

    category, _cls_confidence = engine.classify(message)
    results = engine.retrieve(message, top_k=1)
    top_article, top_score = results[0] if results else (None, 0.0)
    confidence = top_score  # what we show/act on is retrieval match strength, not category confidence

    escalated = confidence < CONFIDENCE_THRESHOLD or top_article is None
    escalation_reason = None
    answer = None
    used_llm = False

    if escalated:
        escalation_reason = (
            "The assistant could not find a confident match in the knowledge base "
            "for this question, so it's being routed to a human agent."
        )
        answer = (
            "I want to make sure you get this right, so I'm looping in a human agent "
            "who'll follow up shortly."
        )
    else:
        answer, used_llm = generate_answer(message, top_article)

    priority = "High" if escalated else "Normal"
    ticket_title = message[:60] + ("..." if len(message) > 60 else "")

    ticket_id = db.create_ticket(
        title=ticket_title,
        message=message,
        category=category,
        confidence=confidence,
        escalated=escalated,
        escalation_reason=escalation_reason,
        answer=answer,
        matched_article_id=top_article["id"] if top_article else None,
        priority=priority,
    )

    return jsonify({
        "ticket_id": ticket_id,
        "category": category,
        "confidence": round(confidence, 3),
        "escalated": escalated,
        "escalation_reason": escalation_reason,
        "answer": answer,
        "used_llm": used_llm,
        "matched_article": top_article["title"] if top_article else None,
    })


@app.route("/api/tickets/<int:ticket_id>/explain")
def api_explain(ticket_id):
    ticket = db.get_ticket(ticket_id)
    if not ticket:
        return jsonify({"error": "not found"}), 404
    article = None
    if ticket["matched_article_id"]:
        article = next((a for a in db.list_kb_articles() if a["id"] == ticket["matched_article_id"]), None)
    explanation = explain_flag(ticket, article)
    return jsonify({"explanation": explanation})


@app.route("/api/tickets/<int:ticket_id>/resolve", methods=["POST"])
def api_resolve(ticket_id):
    db.resolve_ticket(ticket_id)
    return jsonify({"ok": True})


@app.route("/api/kb", methods=["POST"])
def api_add_kb():
    data = request.get_json(force=True)
    db.add_kb_article(
        category=data.get("category", "General"),
        title=data.get("title", "").strip(),
        content=data.get("content", "").strip(),
        keywords=data.get("keywords", "").strip(),
    )
    engine.fit()  # rebuild the TF-IDF index so the new article is searchable immediately
    return jsonify({"ok": True})


@app.route("/api/kb/<int:article_id>/delete", methods=["POST"])
def api_delete_kb(article_id):
    db.delete_kb_article(article_id)
    engine.fit()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
