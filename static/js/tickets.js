document.querySelectorAll(".explain-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const id = btn.dataset.id;
    const box = document.getElementById("explain-" + id);
    if (box.classList.contains("show")) {
      box.classList.remove("show");
      return;
    }
    box.textContent = "Thinking...";
    box.classList.add("show");
    const res = await fetch(`/api/tickets/${id}/explain`);
    const data = await res.json();
    box.textContent = data.explanation;
  });
});

document.querySelectorAll(".resolve-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const id = btn.dataset.id;
    await fetch(`/api/tickets/${id}/resolve`, { method: "POST" });
    window.location.reload();
  });
});
