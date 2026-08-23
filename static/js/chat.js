const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const chatEmpty = document.getElementById("chatEmpty");

function showMessagesView() {
  chatEmpty.style.display = "none";
  chatMessages.classList.add("show");
}

function addUserMessage(text) {
  const el = document.createElement("div");
  el.className = "msg-user";
  el.textContent = text;
  chatMessages.appendChild(el);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
  const wrap = document.createElement("div");
  wrap.className = "msg-bot";
  wrap.id = "typingIndicator";
  wrap.innerHTML = `<div class="msg-bot-bubble typing"><span></span><span></span><span></span></div>`;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
  const el = document.getElementById("typingIndicator");
  if (el) el.remove();
}

function addBotMessage(data) {
  const wrap = document.createElement("div");
  wrap.className = "msg-bot";

  const categoryClass = "badge-" + data.category.toLowerCase().replace(/ /g, "-");
  const confPct = Math.round(data.confidence * 100);

  let escalateHtml = "";
  if (data.escalated) {
    escalateHtml = `<div class="escalate-note">&#9888; ${data.escalation_reason}</div>`;
  }

  wrap.innerHTML = `
    <div class="msg-bot-bubble">${data.answer}</div>
    <div class="msg-meta">
      <span class="badge ${categoryClass}">${data.category}</span>
      <span class="pill">${confPct}% confidence</span>
      ${data.matched_article ? `<span class="pill">Source: ${data.matched_article}</span>` : ""}
      ${data.used_llm ? `<span class="pill">Claude-generated</span>` : ""}
    </div>
    ${escalateHtml}
  `;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(text) {
  if (!text.trim()) return;
  showMessagesView();
  addUserMessage(text);
  addTypingIndicator();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    removeTypingIndicator();
    addBotMessage(data);
  } catch (err) {
    removeTypingIndicator();
    const wrap = document.createElement("div");
    wrap.className = "msg-bot";
    wrap.innerHTML = `<div class="msg-bot-bubble">Something went wrong reaching the server. Is app.py running?</div>`;
    chatMessages.appendChild(wrap);
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = chatInput.value;
  chatInput.value = "";
  sendMessage(text);
});

document.querySelectorAll(".suggest-chip").forEach((btn) => {
  btn.addEventListener("click", () => sendMessage(btn.dataset.q));
});
