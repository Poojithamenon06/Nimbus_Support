"""
Optional generation layer, this is the 'G' in RAG.

If ANTHROPIC_API_KEY is set in .env, we ask Claude to write a short,
natural-language answer that is STRICTLY grounded in the retrieved
article (we pass the article text in the prompt and instruct it not to
add anything not in that text). If no key is set, we skip generation
entirely and just return the matched article's own content, still fully
grounded and correct, just not paraphrased into a conversational tone.

This fallback is intentional: a reviewer should be able to clone this repo
and see it work with zero setup, an API key is a nice-to-have, not a
dependency.
"""
import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

_client = None
if ANTHROPIC_API_KEY:
    try:
        import anthropic
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    except Exception:
        _client = None


def generate_answer(user_question, article):
    """Return (answer_text, used_llm: bool)."""
    if _client is None:
        # fallback: pure retrieval, no generation
        return article["content"], False

    prompt = (
        "You are a Tier-1 customer support assistant. Answer the user's question "
        "using ONLY the information in the article below. Do not add any fact that "
        "isn't in the article. Keep the answer under 80 words and conversational.\n\n"
        f"Article title: {article['title']}\n"
        f"Article content: {article['content']}\n\n"
        f"User question: {user_question}\n\n"
        "Answer:"
    )
    try:
        resp = _client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in resp.content if block.type == "text").strip()
        return (text or article["content"]), True
    except Exception:
        return article["content"], False


def explain_flag(ticket, article):
    """Used by the 'why was this flagged / escalated' feature."""
    if _client is None:
        return (
            f"This ticket was routed to '{ticket['category']}' with "
            f"{round(ticket['confidence']*100)}% match confidence against the article "
            f"'{article['title']}'." if article else
            f"This ticket had low similarity ({round(ticket['confidence']*100)}%) to any "
            f"knowledge base article, so it was escalated to a human."
        )
    prompt = (
        "Explain in one or two plain-English sentences why this support ticket was handled "
        f"the way it was. Category assigned: {ticket['category']}. Confidence score: "
        f"{round(ticket['confidence']*100)}%. Escalated: {bool(ticket['escalated'])}. "
        f"Escalation reason (if any): {ticket.get('escalation_reason') or 'none'}. "
        f"Matched article: {article['title'] if article else 'none'}."
    )
    try:
        resp = _client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in resp.content if block.type == "text").strip()
    except Exception:
        return f"Routed to {ticket['category']} at {round(ticket['confidence']*100)}% confidence."
