import sys
import time
from pathlib import Path

import streamlit as st

# ── Allow importing from the app/ directory ──────────────────────────────────
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from rag import ask_question, RAGResult  # noqa: E402


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AshuuAI — Antigone Scholar",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto",   # collapses on mobile automatically
)


# ══════════════════════════════════════════════════════════════════════════════
#  CSS  —  Fully Responsive Premium Dark GPT-style UI + animations
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

/* ── Base / Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
}

.stApp { background: #080a12; color: #e2e4f0; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Main content container — fluid width ── */
.block-container {
    max-width: 860px !important;
    width: 100% !important;
    padding: 1rem 1.2rem !important;
    margin: 0 auto !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0e1020;
    border-right: 1px solid #1a1d35;
    min-width: 220px !important;
    max-width: 280px !important;
}
section[data-testid="stSidebar"] * { color: #b0b3cc !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #9d7fea !important; }

/* ── Chat bubbles ── */
.msg-user {
    background: linear-gradient(135deg, #1c1f38 0%, #181b30 100%);
    border: 1px solid #2a2e50;
    border-radius: 16px 16px 4px 16px;
    padding: 14px 20px;
    margin: 10px 0 10px clamp(8px, 5vw, 40px);
    max-width: 88%;
    width: fit-content;
    margin-left: auto;
    color: #dde0f5;
    line-height: 1.7;
    font-size: clamp(0.85rem, 2.2vw, 0.95rem);
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    word-break: break-word;
    overflow-wrap: anywhere;
}
.msg-assistant {
    background: linear-gradient(135deg, #111328 0%, #0f1122 100%);
    border: 1px solid #1e2245;
    border-left: 3px solid #8b5cf6;
    border-radius: 4px 16px 16px 16px;
    padding: clamp(12px, 3vw, 18px) clamp(14px, 3.5vw, 22px);
    margin: 10px clamp(8px, 5vw, 40px) 10px 0;
    max-width: 94%;
    color: #d4d6ee;
    line-height: 1.8;
    font-size: clamp(0.85rem, 2.2vw, 0.96rem);
    box-shadow: 0 2px 16px rgba(139,92,246,0.08);
    word-break: break-word;
    overflow-wrap: anywhere;
}
.msg-error {
    background: #160d10;
    border: 1px solid #5a1a2a;
    border-left: 3px solid #dc4c6e;
    border-radius: 4px 16px 16px 16px;
    padding: 14px 20px;
    margin: 10px clamp(8px, 5vw, 40px) 10px 0;
    max-width: 94%;
    color: #f0a0b5;
    font-size: clamp(0.82rem, 2vw, 0.93rem);
    line-height: 1.7;
}
.msg-assistant p { margin: 0.4em 0; }
.msg-assistant ul, .msg-assistant ol { margin: 0.3em 0 0.3em 1.2em; }
.msg-assistant li { margin: 0.25em 0; }
.msg-assistant strong { color: #c4b5fd; }
.msg-assistant blockquote {
    border-left: 2px solid #7c3aed;
    margin: 8px 0;
    padding-left: 12px;
    color: #a89ad4;
    font-style: italic;
}

/* ── Role labels ── */
.role-user {
    color: #7c6be8; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 12px 0 3px 40px;
}
.role-ai {
    color: #9d7fea; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 12px 0 3px 0;
    display: flex; align-items: center; gap: 6px;
}
.role-err {
    color: #dc4c6e; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 12px 0 3px 0;
}

/* ── TYPING ANIMATION ── */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes pulse-dot {
    0%,100% { transform:scale(1);   opacity:1; }
    50%      { transform:scale(1.4); opacity:0.6; }
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 14px 20px;
    background: linear-gradient(135deg, #111328, #0f1122);
    border: 1px solid #1e2245;
    border-left: 3px solid #8b5cf6;
    border-radius: 4px 16px 16px 16px;
    margin: 10px 40px 10px 0;
    width: fit-content;
}
.typing-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #8b5cf6;
    animation: pulse-dot 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; background: #a78bfa; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; background: #c4b5fd; }

/* ── Streaming text animation ── */
.stream-text {
    animation: fadeInUp 0.4s ease-out;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 48px 0 16px 0;
    animation: fadeInUp 0.6s ease-out;
}
.hero .brand {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa, #c084fc, #7c3aed);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    letter-spacing: -0.02em;
}
.hero .tagline {
    color: #5a5e82;
    font-size: 0.9rem;
    margin: 10px 0 0;
    font-weight: 400;
}
.hero .badge {
    display: inline-block;
    margin-top: 14px;
    background: #141628;
    border: 1px solid #2a2e50;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: #7c6be8;
    font-weight: 500;
}

/* ── Suggestion grid ── */
.sug-label {
    text-align: center;
    color: #3a3d5a;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 28px 0 12px;
}
.stButton > button {
    background: linear-gradient(135deg, #161828, #1a1d35) !important;
    color: #9d8fd8 !important;
    border: 1px solid #252848 !important;
    border-radius: 12px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e2040, #222548) !important;
    border-color: #6d4fc4 !important;
    color: #c4b5fd !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(109,79,196,0.25) !important;
}

/* ── Clear / action buttons get a different style ── */
button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #2a2e50 !important;
    color: #6b6e9a !important;
}

/* ── Send button specifically ── */
.stForm button[type="submit"] {
    background: linear-gradient(135deg, #7c3aed, #9d7fea) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 12px 20px !important;
    transition: all 0.2s !important;
}
.stForm button[type="submit"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Input ── */
.stTextArea textarea {
    background: #0e1020 !important;
    border: 1px solid #252848 !important;
    border-radius: 14px !important;
    color: #e0e2f4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.96rem !important;
    resize: none !important;
    line-height: 1.6 !important;
    min-height: 60px !important;
    width: 100% !important;
    touch-action: manipulation;
}
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important;
}
.stTextArea textarea::placeholder { color: #3a3d5a !important; }

hr { border-color: #1a1d35 !important; margin: 16px 0 !important; }

/* ── Scrollable chat ── */
.chat-wrap { padding: 4px 0; }

/* ══════════════════════════════════════════════
   RESPONSIVE — Tablet  (≤ 768px)
══════════════════════════════════════════════ */
@media (max-width: 768px) {
    .block-container {
        padding: 0.6rem 0.8rem !important;
    }

    /* Sidebar auto-hides on mobile — collapse it */
    section[data-testid="stSidebar"] {
        min-width: 0 !important;
        max-width: 260px !important;
    }

    /* Hero scaling */
    .hero { padding: 28px 0 12px; }
    .hero .brand { font-size: 2.2rem; }
    .hero .tagline { font-size: 0.82rem; }
    .hero .badge { font-size: 0.7rem; padding: 3px 10px; }

    /* Bubbles — tighter margins */
    .msg-user    { margin-left: 6px;  max-width: 96%; font-size: 0.9rem; }
    .msg-assistant{ margin-right: 6px; max-width: 96%; font-size: 0.9rem; }
    .msg-error   { margin-right: 6px; max-width: 96%; }

    .role-user { margin-left: 6px; }

    /* Typing indicator */
    .typing-indicator { margin-right: 6px; padding: 10px 14px; }

    /* Input row — stack vertically on tablet */
    .stForm [data-testid="column"]:first-child { min-width: 100% !important; }

    /* Buttons — larger touch targets */
    .stButton > button {
        font-size: 0.8rem !important;
        padding: 10px 10px !important;
        min-height: 44px !important;
    }
    .stForm button[type="submit"] {
        min-height: 44px !important;
        font-size: 0.9rem !important;
    }

    /* Suggestion label */
    .sug-label { margin: 18px 0 8px; font-size: 0.68rem; }
}

/* ══════════════════════════════════════════════
   RESPONSIVE — Mobile  (≤ 480px)
══════════════════════════════════════════════ */
@media (max-width: 480px) {
    .block-container {
        padding: 0.4rem 0.5rem !important;
    }

    /* Hero — compact */
    .hero { padding: 20px 0 8px; }
    .hero .brand {
        font-size: 1.8rem;
        letter-spacing: -0.01em;
    }
    .hero .tagline { font-size: 0.78rem; }
    .hero .badge { display: none; }  /* hide badge on very small screens */

    /* Bubbles — full width, minimal margin */
    .msg-user {
        margin: 6px 0 6px 0;
        max-width: 100%;
        padding: 10px 14px;
        border-radius: 12px 12px 4px 12px;
        font-size: 0.88rem;
    }
    .msg-assistant {
        margin: 6px 0;
        max-width: 100%;
        padding: 10px 14px;
        border-radius: 4px 12px 12px 12px;
        font-size: 0.88rem;
        line-height: 1.7;
    }
    .msg-error {
        margin: 6px 0;
        max-width: 100%;
        padding: 10px 14px;
    }
    .msg-assistant ul, .msg-assistant ol {
        margin-left: 0.9em;
    }

    /* Role labels */
    .role-user  { margin-left: 2px; font-size: 0.65rem; }
    .role-ai    { font-size: 0.65rem; }
    .role-err   { font-size: 0.65rem; }

    /* Typing dots — smaller */
    .typing-indicator { padding: 8px 12px; gap: 4px; margin-right: 0; }
    .typing-dot { width: 6px; height: 6px; }

    /* Suggestion chips — 2 columns on phone */
    /* (Streamlit columns will wrap naturally) */
    .stButton > button {
        font-size: 0.76rem !important;
        padding: 8px 8px !important;
        min-height: 42px !important;
        border-radius: 10px !important;
    }

    /* Send button — full width on mobile */
    .stForm button[type="submit"] {
        width: 100% !important;
        min-height: 46px !important;
        font-size: 0.88rem !important;
        margin-top: 6px !important;
    }

    /* Textarea full width */
    .stTextArea textarea {
        font-size: 0.9rem !important;
        min-height: 70px !important;
        border-radius: 10px !important;
    }

    /* Sug label */
    .sug-label { font-size: 0.65rem; margin: 14px 0 6px; }

    hr { margin: 10px 0 !important; }
}

/* ══════════════════════════════════════════════
   RESPONSIVE — Large desktop  (≥ 1200px)
══════════════════════════════════════════════ */
@media (min-width: 1200px) {
    .block-container { max-width: 900px !important; }
    .hero .brand { font-size: 3.4rem; }
    .msg-user    { font-size: 0.97rem; }
    .msg-assistant{ font-size: 0.97rem; }
}
</style>
""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rate_limit_until" not in st.session_state:
    st.session_state.rate_limit_until = 0
if "input_text" not in st.session_state:
    st.session_state.input_text = ""


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<div style='padding:8px 0 4px'>"
        "<span style='font-size:1.5rem;font-weight:800;"
        "background:linear-gradient(135deg,#8b5cf6,#c084fc);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "background-clip:text'>✨ AshuuAI</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<span style='color:#4a4e6e;font-size:0.82rem'>"
        "RAG Scholar for Sophocles' <em>Antigone</em></span>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("### 💡 What you can ask")
    st.markdown("""
- 🎭 **Scene summaries**
- 👤 **Character deep-dives**
- 📖 **Theme analysis**
- 🎓 **1 / 2 / 5 / 10-mark questions**
- 💬 **Dialogue explanations**
- 📜 **Quotes & their meaning**
- 🔍 **Conflict analysis**
- 📝 **Essay-style answers**
""")
    st.divider()

    col1, col2 = st.columns(2)
    if col1.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.rate_limit_until = 0
        st.rerun()

    st.markdown(
        "<br><span style='color:#2e3155;font-size:0.75rem'>"
        "Model · Llama 3.3-70B (Groq)<br>"
        "Embeddings · MiniLM-L6-v2<br>"
        "Vector DB · FAISS</span>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  HERO  (only shown when no chat history)
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.messages:
    st.markdown("""
<div class='hero'>
  <div class='brand'>✨ AshuuAI</div>
  <div class='tagline'>Your AI scholar for Sophocles' <em>Antigone</em></div>
  <div class='badge'>📚 Powered by RAG · Groq · FAISS</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='sug-label'>✦ Try asking one of these</div>", unsafe_allow_html=True)

    SUGGESTIONS = [
        "📖 Summarise the opening scene",
        "🎓 Give me 5 ten-mark exam questions",
        "👤 Who is Antigone? What drives her?",
        "⚔️ Explain the conflict between Antigone and Creon",
        "📜 Generate 1-mark questions from the play",
        "💀 What happens to Haemon at the end?",
        "🌟 What is the theme of divine law vs civil law?",
        "💬 Explain the argument between Creon and his son",
        "🎭 Summarise the scene where Tiresias warns Creon",
        "📝 Give me 2-mark questions about Ismene",
        "❝ Quote Antigone speaking about her duty",
        "🔍 Who is Tiresias and what is his role?",
    ]

    # 2-column grid — works on both mobile and desktop
    col_a, col_b = st.columns(2)
    for i, sug in enumerate(SUGGESTIONS):
        target_col = col_a if i % 2 == 0 else col_b
        if target_col.button(sug, key=f"sug_{i}", use_container_width=True):
            st.session_state.input_text = sug.split(" ", 1)[1] if " " in sug else sug
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
def render_message(role: str, content: str, status: str = "ok"):
    if role == "user":
        st.markdown(
            f"<div class='role-user'>You</div>"
            f"<div class='msg-user stream-text'>{content}</div>",
            unsafe_allow_html=True,
        )
    elif status in ("rate_limit", "error"):
        st.markdown(
            f"<div class='role-err'>⚠ System Alert</div>"
            f"<div class='msg-error stream-text'>{content}</div>",
            unsafe_allow_html=True,
        )
    else:
        # Render markdown properly inside the styled div
        st.markdown(
            f"<div class='role-ai'>✨ AshuuAI</div>",
            unsafe_allow_html=True,
        )
        with st.container():
            st.markdown(
                f"<div class='msg-assistant stream-text'>",
                unsafe_allow_html=True,
            )
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("status", "ok"))
st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  RATE-LIMIT COUNTDOWN
# ══════════════════════════════════════════════════════════════════════════════
now = time.time()
if st.session_state.rate_limit_until > now:
    remaining = int(st.session_state.rate_limit_until - now)
    st.markdown(
        f"""<div style='background:#160d10;border:1px solid #5a1a2a;
        border-left:3px solid #dc4c6e;border-radius:12px;padding:16px 20px;
        margin:12px 0;'>
        <span style='color:#dc4c6e;font-weight:700;font-size:1rem'>
        🔴 Rate Limit Reached</span><br>
        <span style='color:#d88090;font-size:0.9rem'>
        Groq API cooling down — please wait
        <b style='color:#f0a0b5;font-size:1.1rem'>{remaining}s</b> ⏳
        </span></div>""",
        unsafe_allow_html=True,
    )
    time.sleep(1)
    st.rerun()
else:
    if st.session_state.rate_limit_until != 0:
        st.session_state.rate_limit_until = 0


# ══════════════════════════════════════════════════════════════════════════════
#  INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════
st.divider()

with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_area(
            label="Message",
            value=st.session_state.input_text,
            placeholder="Ask anything about Antigone…  (e.g. Summarise the trial scene)",
            height=90,
            label_visibility="collapsed",
            key="user_input",
        )
    with col_btn:
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Send ➤", use_container_width=True)

st.session_state.input_text = ""


# ══════════════════════════════════════════════════════════════════════════════
#  HANDLE SUBMISSION  +  TYPING ANIMATION
# ══════════════════════════════════════════════════════════════════════════════
if submitted and user_input and user_input.strip():
    question = user_input.strip()

    # 1. Save user bubble
    st.session_state.messages.append({"role": "user", "content": question})
    render_message("user", question)

    # 2. Show animated typing indicator while waiting
    st.markdown("<div class='role-ai'>✨ AshuuAI</div>", unsafe_allow_html=True)
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        "<div class='typing-indicator'>"
        "<div class='typing-dot'></div>"
        "<div class='typing-dot'></div>"
        "<div class='typing-dot'></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # 3. Call RAG
    result: RAGResult = ask_question(question)

    # 4. Clear typing indicator
    typing_placeholder.empty()

    if result.status == "ok":
        # Simulate streaming: reveal text word by word into a placeholder
        stream_placeholder = st.empty()
        words = result.answer.split()
        displayed = ""
        for i, word in enumerate(words):
            displayed += word + " "
            # Update every few words for smooth feel without too many rerenders
            if i % 4 == 0 or i == len(words) - 1:
                stream_placeholder.markdown(
                    f"<div class='msg-assistant'>{displayed}▌</div>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.025)
        # Final render without cursor
        stream_placeholder.markdown(
            f"<div class='msg-assistant stream-text'>{result.answer}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": result.answer, "status": "ok"}
        )

    elif result.status == "out_of_scope":
        st.markdown(
            f"<div class='msg-assistant stream-text'>{result.answer}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": result.answer, "status": "out_of_scope"}
        )

    elif result.status == "rate_limit":
        wait = result.wait_seconds
        st.session_state.rate_limit_until = time.time() + wait
        msg = (
            f"🔴 **Token / Rate Limit Reached**\n\n"
            f"The Groq API has throttled this request. "
            f"Please wait **{wait} seconds** before trying again.\n\n"
            f"> _{result.error_detail[:200]}_"
        )
        st.markdown(
            f"<div class='msg-error'>{msg}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": msg, "status": "rate_limit"}
        )

    else:
        msg = (
            f"❌ **Unexpected error.**\n\n"
            f"`{result.error_detail[:300]}`\n\nPlease try again."
        )
        st.markdown(
            f"<div class='msg-error'>{msg}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": msg, "status": "error"}
        )

    st.rerun()
