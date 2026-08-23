const newArticleBtn = document.getElementById("newArticleBtn");
const kbForm = document.getElementById("kbForm");
const cancelKbBtn = document.getElementById("cancelKbBtn");
const saveKbBtn = document.getElementById("saveKbBtn");

newArticleBtn.addEventListener("click", () => {
  kbForm.style.display = kbForm.style.display === "none" ? "block" : "none";
});

cancelKbBtn.addEventListener("click", () => {
  kbForm.style.display = "none";
});

saveKbBtn.addEventListener("click", async () => {
  const category = document.getElementById("kbCategory").value;
  const title = document.getElementById("kbTitle").value.trim();
  const content = document.getElementById("kbContent").value.trim();
  const keywords = document.getElementById("kbKeywords").value.trim();

  if (!title || !content) {
    alert("Title and content are required.");
    return;
  }

  await fetch("/api/kb", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, title, content, keywords }),
  });
  window.location.reload();
});

document.querySelectorAll(".kb-delete").forEach((btn) => {
  btn.addEventListener("click", async () => {
    if (!confirm("Delete this article?")) return;
    await fetch(`/api/kb/${btn.dataset.id}/delete`, { method: "POST" });
    window.location.reload();
  });
});
