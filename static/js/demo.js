/* ============================= */
/* OMINEX DEMO — STATIC JS (FIXED)
   - Keeps: bubbles, typing, voice, unlock, demo replies
   - Adds: intro speaks ON FIRST user interaction (browser-safe)
   - Adds: backend optional (/api/demo). If backend fails → static demoReply fallback
   - Does NOT remove your core features
*/
/* ============================= */

(() => {
  /* ---------- DOM ---------- */
const chat = document.getElementById("chat");
const input = document.getElementById("input");

  if (!chat || !input) {
    console.error("[OMINEX] Missing #chat or #input in HTML");
    return;
  }

  /* ---------- STATE ---------- */
  let voiceUnlocked = false;
  let introSpoken = false;
  let selectedVoice = null;

  /* ---------- UI: ADD MESSAGE ---------- */
function add(role, text) {
    const msg = document.createElement("div");
    msg.className = "msg " + role;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    msg.appendChild(bubble);
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;

    return bubble; // allow typing into bubble
  }

  /* ---------- UI: TYPING EFFECT ---------- */
function typeReply(text, onDone) {
    const bubble = add("bot", ""); // empty bubble, then type into it

    let i = 0;
    const speed = 18;

    const interval = setInterval(() => {
      bubble.textContent += text.charAt(i);
      i++;
      chat.scrollTop = chat.scrollHeight;

      if (i >= text.length) {
        clearInterval(interval);
        if (typeof onDone === "function") onDone();
      }
    }, speed);
  }

  /* ---------- VOICE: PICK VOICE ---------- */
function pickVoice() {
    const voices = speechSynthesis.getVoices() || [];
    if (!voices.length) return null;

    // Prefer “female-ish” English voices (Windows/Edge/Chrome vary)
    const preferred =
      voices.find(v => v.lang?.toLowerCase().startsWith("en") && /aria|jenny|sonia|zira|female|susan/i.test(v.name)) ||
      voices.find(v => v.lang?.toLowerCase().startsWith("en")) ||
      voices[0];

    return preferred || null;
  }

  /* ---------- VOICE: UNLOCK ---------- */
function unlockVoice() {
    if (voiceUnlocked) return;

    try {
      // Warm voices list (sometimes empty until called after gesture)
      speechSynthesis.getVoices();
      selectedVoice = pickVoice();
      voiceUnlocked = true;
      console.log("🔊 [OMINEX] Voice unlocked");
    } catch (e) {
      console.warn("[OMINEX] unlockVoice failed:", e);
    }
  }

  /* ---------- VOICE: SPEAK ---------- */
function speak(text) {
    if (!("speechSynthesis" in window)) return;
    if (!voiceUnlocked) return;

    const msg = (text || "").trim();
    if (!msg) return;

    try {
      const utter = new SpeechSynthesisUtterance(msg);
      utter.rate = 0.92;   // calm
      utter.pitch = 1.12;  // slightly feminine (safe across voices)
      utter.volume = 1;

      // Ensure voice exists (sometimes arrives late)
      if (!selectedVoice) selectedVoice = pickVoice();
      if (selectedVoice) {
        utter.voice = selectedVoice;
        utter.lang = selectedVoice.lang || "en-US";
      } else {
        utter.lang = "en-US";
      }

      speechSynthesis.cancel();
      speechSynthesis.speak(utter);
    } catch (e) {
      console.warn("[OMINEX] speak() failed:", e);
    }
  }

  // Keep voices updated if the browser loads them later
  window.speechSynthesis.onvoiceschanged = () => {
    if (!selectedVoice) selectedVoice = pickVoice();
  };

  /* ---------- DEMO INTELLIGENCE (STATIC FALLBACK) ---------- */
function demoReply(text) {
    const t = (text || "").toLowerCase();

    if (t.includes("who made") || t.includes("who created") || t.includes("creator")) {
      return "I was created by Luvo Maphela as part of the OMINEX system.";
    }
    if (t === "hi" || t.includes("hello") || t.includes("hey")) {
      return "Hello. OMINEX online.";
    }
    if (t.includes("native language") || t.includes("language")) {
      return "I do not have a native language. I process and generate text across multiple languages.";
    }
    if (t.includes("help") || t.includes("what can you do")) {
      return "This is a demonstration interface. Advanced cognition is currently disabled. Ask simple questions to test presentation and interaction.";
    }
    if (t.includes("what are you") || t.includes("who are you")) {
      return "I am OMINEX — a controlled demo assistant designed for premium presentation and interaction.";
    }

    return "I am a controlled demo instance. My purpose is presentation.";
  }

  /* ---------- BACKEND (OPTIONAL) ---------- */
async function tryBackendReply(userText) {
  const res = await fetch("https://ominex-backend.onrender.com/api/demo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error("Backend error: " + t);
  }

  const data = await res.json();
  if (!data || !data.reply) throw new Error("No reply in payload");
  return String(data.reply);
}

  /* ---------- INTRO: SPEAK ON FIRST GESTURE ---------- */
function speakIntroOnce() {
    if (introSpoken) return;
    introSpoken = true;

    const intro =
      "I am OMINEX. An intelligent demonstration assistant designed for presentation and interaction. You may ask me anything.";

    // Type + speak (after unlock)
    typeReply(intro, () => speak(intro));
  }

  /* ---------- INPUT HANDLER ---------- */
input.addEventListener("keydown", (e) => {
  if (e.key !== "Enter") return;

  // 🔓 Always unlock + intro on first Enter
  unlockVoice();
  speakIntroOnce();

  const text = input.value.trim();

  // ✅ If first Enter is ONLY to activate voice, stop here
  if (!text) {
    input.value = "";
    return;
  }

input.value = "";
  add("user", text);

  setTimeout(async () => {
    let reply = "";
    try {
      reply = await tryBackendReply(text);
    } catch {
      reply = demoReply(text);
    }

    typeReply(reply, () => speak(reply));
  }, 420);
});

  /* ---------- BOOT MESSAGE (TEXT ONLY) ---------- */
  add("bot", "Hi. I’m OMINEX (demo). Press Enter once to activate voice.");

  add("bot", "🔊 Press Enter or click anywhere to activate voice.");


  // Optional: also unlock on any click/tap (nice UX)
document.addEventListener(
    "click",
    () => {
      unlockVoice();
      speakIntroOnce();
    },
    { once: true }
  );
})();

