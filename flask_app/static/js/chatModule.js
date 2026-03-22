


/**
 * CityFlow — chatModule.js
 * =========================
 * Pre-written Q&A chatbot.
 * No API key needed — all answers come from the Flask backend.
 *
 * Flow:
 *   1. Page loads → fetch /api/chat/categories → show category buttons
 *   2. User clicks a category → show its 2 questions
 *   3. User clicks a question → POST /api/chat/answer → show typed-out answer
 *   4. Back button → return to categories
 */
 
document.addEventListener("DOMContentLoaded", () => {
  loadCategories();
  document.getElementById("clearBtn").addEventListener("click", clearChat);
  document.getElementById("backBtn").addEventListener("click", showCategories);
});
 
// ── Load categories from Flask ────────────────────────────────────────────────
async function loadCategories() {
  try {
    const res  = await fetch("/api/chat/categories");
    const data = await res.json();
    renderCategories(data);
  } catch (err) {
    console.error("Failed to load categories:", err);
    document.getElementById("catList").innerHTML =
      '<p style="font-size:0.8rem;color:#8FA5BB;padding:0.5rem">Could not load topics. Is Flask running?</p>';
  }
}
 
// ── Render category buttons in sidebar ───────────────────────────────────────
function renderCategories(categories) {
  const list = document.getElementById("catList");
  list.innerHTML = "";
 
  categories.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = "cat-btn";
    btn.innerHTML = `
      <span class="cat-icon">${cat.icon}</span>
      <div>
        <div class="cat-label">${cat.label}</div>
        <div class="cat-count">${cat.questions.length} questions</div>
      </div>
      <span class="cat-arrow">›</span>`;
 
    btn.addEventListener("click", () => showQuestions(cat));
    list.appendChild(btn);
  });
}
 
// ── Show questions for a category ────────────────────────────────────────────
function showQuestions(cat) {
  // Hide category list, show question panel
  document.getElementById("catList").style.display        = "none";
  document.getElementById("questionPanel").style.display  = "flex";
  document.getElementById("questionCatLabel").textContent = `${cat.icon} ${cat.label}`;
 
  const qList = document.getElementById("qList");
  qList.innerHTML = "";
 
  cat.questions.forEach(q => {
    const btn = document.createElement("button");
    btn.className   = "q-btn";
    btn.textContent = q.question;
    btn.addEventListener("click", () => selectQuestion(q, cat.label, btn));
    qList.appendChild(btn);
  });
 
  // Show the user's selection in chat
  showCategoryPrompt(cat);
}
 
// ── Back to categories
function showCategories() {
  document.getElementById("catList").style.display       = "block";
  document.getElementById("questionPanel").style.display = "none";
 
  // Remove active states
  document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
}
 
// ── User clicked a question
async function selectQuestion(q, catLabel, btn) {
  // Mark active
  document.querySelectorAll(".q-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
 
  // Hide the bottom prompt
  document.getElementById("chatPrompt").style.display = "none";
 
  // Show user bubble with the question
  appendMsg("user", q.question);
 
  // Show typing animation
  setTyping(true);
 
  try {
    const res  = await fetch("/api/chat/answer", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ question_id: q.id }),
    });
    const data = await res.json();
 
    // Small delay so typing animation feels natural
    await sleep(700);
    setTyping(false);
 
    if (data.error) {
      appendMsg("bot", "Sorry, I couldn't find an answer for that. Please try another question.");
    } else {
      appendMsg("bot", data.answer, catLabel);
    }
  } catch (err) {
    await sleep(500);
    setTyping(false);
    appendMsg("bot", "⚠️ Couldn't connect to the server. Make sure Flask is running.");
    console.error("Answer fetch failed:", err);
  }
}
 
//  Append a message bubble 
function appendMsg(role, text, catLabel = null) {
  const msgs  = document.getElementById("chatMsgs");
  const isBot = role === "bot";
  const time  = new Date().toLocaleTimeString("en-IE", { hour: "2-digit", minute: "2-digit" });
 
  const botIcon  = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="13" height="13"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`;
  const userIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="13" height="13"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
 
  // Format text: **bold** → <strong>, newlines → <br>
  const html = escapeHTML(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
 
  // Category chip (shown above bot answers)
  const chipHTML = (isBot && catLabel)
    ? `<div class="msg-cat-chip">${catLabel}</div>`
    : "";
 
  const div = document.createElement("div");
  div.className = `msg msg-${isBot ? "bot" : "user"}`;
  div.innerHTML = `
    <div class="msg-ava ${isBot ? "bot" : "user"}">${isBot ? botIcon : userIcon}</div>
    <div class="msg-body">
      ${chipHTML}
      <div class="msg-bub">${html}</div>
      <span class="msg-time">${time}</span>
    </div>`;
 
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}
 
// ── Show category selection in chat 
function showCategoryPrompt(cat) {
  // Only show if chat is still at the welcome state
  const msgs = document.getElementById("chatMsgs");
  if (msgs.querySelectorAll(".msg").length <= 1) {
    appendMsg("bot", `Great choice! Here are questions about **${cat.label}**. Click one on the left to get an answer. 👈`);
  }
}
 
// ── Typing indicator
function setTyping(show) {
  const el = document.getElementById("chatTyping");
  if (!el) return;
  el.style.display = show ? "flex" : "none";
  if (show) {
    const msgs = document.getElementById("chatMsgs");
    msgs.scrollTop = msgs.scrollHeight;
  }
}
 
// ── Clear chat ────────────────────────────────────────────────────────────────
function clearChat() {
  const msgs = document.getElementById("chatMsgs");
  // Remove everything except the welcome message (first .msg)
  const all = msgs.querySelectorAll(".msg");
  all.forEach((m, i) => { if (i > 0) m.remove(); });
 
  // Show bottom prompt again
  document.getElementById("chatPrompt").style.display = "block";
 
  // Reset sidebar
  showCategories();
  document.querySelectorAll(".q-btn").forEach(b => b.classList.remove("active"));
}
 
// ── Utilities ─────────────────────────────────────────────────────────────────
function escapeHTML(str) {
  return str
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;");
}
 
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
