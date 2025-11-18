import streamlit as st
import chatbot_backend as demo
import login
import os
from streamlit_lottie import st_lottie
import json


# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="App Inventor Assistant",
    page_icon="🤖",
    layout="wide"
)

def load_lottie(path):
    with open(path, "r") as f:
        return json.load(f)


# Load external CSS file
css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ================= LOTTIES =================
# Load one main Lottie animation
lottie_main = load_lottie("lotties/robot.json")

# Floating Lottie container (CSS will position it)
st.markdown('<div id="floating-lottie"></div>', unsafe_allow_html=True)

# Render the Lottie animation invisibly — we will reposition using CSS
st_lottie(
    lottie_main,
    key="main-lottie",
    height=300,
    speed=1.0,
    loop=True,
)



# ============= AUTH (still bypassed) =============
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # <- bypass login for now

# if not st.session_state["authenticated"]:
#     login.login()
#     st.stop()
# =================================================

# ============= SESSION STATE INIT ================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "referred_doc" not in st.session_state:
    st.session_state.referred_doc = None
if "doc_open" not in st.session_state:
    st.session_state.doc_open = False
if "assistant_mode" not in st.session_state:
    st.session_state.assistant_mode = "Tutor"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2  # reserved for later use
# =================================================


# ================== SIDEBAR ======================
with st.sidebar:
    st.header("Settings ⚙️")

    # Assistant "mode" – you can later wire this into your prompt if you want
    st.session_state.assistant_mode = st.selectbox(
        "Assistant style",
        ["Tutor", "Debugger", "Idea Generator", "Step-by-step Coach"],
        index=["Tutor", "Debugger", "Idea Generator", "Step-by-step Coach"].index(
            st.session_state.assistant_mode
        )
    )

    st.session_state.temperature = st.slider(
        "Creativity (for future use)",
        0.0, 1.0, st.session_state.temperature, 0.05
    )

    st.markdown("---")

    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.referred_doc = None
        st.session_state.doc_open = False
        st.success("Chat history cleared!")

    #if st.session_state.referred_doc != "No document was searched":
    if st.button("📄 Toggle Referred Document Panel"):
        st.session_state.doc_open = not st.session_state.doc_open

    st.markdown("---")
    st.caption("Pro tip: Ask things like\n“Help me debug my blocks” or\n“Explain how the Clock component works.”")
# =================================================


# ================== HEADER SECTION ===============
col_logo, col_title = st.columns([1, 3], gap="large")

with col_logo:
    st.image("logo.png", width=710)

with col_title:
    st.markdown(
        "<div class='app-header'><h1 style='color:#1E88E5;'>App Inventor Assistant 🤖🧱</h1></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#546E7A;'>"
        "Ask questions about MIT App Inventor blocks, debugging, and project ideas."
        "</p>",
        unsafe_allow_html=True
    )

st.markdown("---")
# =================================================


# =============== HELPER: PROCESS MESSAGE =========
def handle_user_message(user_text: str):
    """Send user_text to backend and update chat + referred doc in session."""
    # Show user message
    st.chat_message("user", avatar="🧑‍🎓").markdown(user_text)
    st.session_state.chat_history.append({"role": "user", "text": user_text})

    # Call backend
    chat_response = demo.demo_conversation(user_text)

    # Split assistant main text vs. referred document
    if "**Referred Document**:" in chat_response:
        main_response, referred_doc = chat_response.split("**Referred Document**:")
        main_response = main_response.strip()
        referred_doc = referred_doc.strip()
    else:
        main_response = chat_response
        referred_doc = None

    # Show assistant message
    st.chat_message("assistant", avatar="🤖").markdown(main_response)
    st.session_state.chat_history.append({"role": "assistant", "text": main_response})

    # Update referred document + auto-open panel if it's real content
    st.session_state.referred_doc = referred_doc
    if referred_doc and referred_doc != "No document was searched":
        st.session_state.doc_open = True
# =================================================


# ================== RENDER OLD CHAT ==============
for msg in st.session_state.chat_history:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
    st.chat_message(msg["role"], avatar=avatar).markdown(msg["text"])
# =================================================


# ================== CHAT INPUT ===================
input_text = st.chat_input("💬 Ask me anything about App Inventor...")
trigger_sent = False

if input_text:
    trigger_sent = True
    handle_user_message(input_text)

# ============== SUGGESTED PROMPTS ROW ============
st.markdown("<div class='suggested-prompts'>Try one of these:</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔍 Explain a block", use_container_width=True):
        if not trigger_sent:
            handle_user_message("Explain how the 'if-then-else' block works in App Inventor.")
            trigger_sent = True

with c2:
    if st.button("🐞 Help me debug", use_container_width=True):
        if not trigger_sent:
            handle_user_message("I'm getting an error when I click a button. Can you help me debug?")
            trigger_sent = True

with c3:
    if st.button("💡 Project idea", use_container_width=True):
        if not trigger_sent:
            handle_user_message("Give me a simple project idea to practice using lists and timers in App Inventor.")
            trigger_sent = True
# =================================================


# ============== REFERRED DOC SLIDE PANEL =========
doc_container_class = "open" if st.session_state.doc_open else ""
doc_content = st.session_state.referred_doc if st.session_state.referred_doc else "No referred document"

if doc_content and doc_content != "No document was searched":
    panel_content = f"""
    <div id="referred-doc" class="{doc_container_class}">
        <h3>📄 Referred Document</h3>
        <p style="font-size:0.85rem; color:#607D8B;">
            This is a snippet that the assistant used while answering.
        </p>
        <hr/>
        <div>{doc_content}</div>
    </div>
    """
else:
    panel_content = f'<div id="referred-doc" class="{doc_container_class}">No referred document</div>'

st.markdown(panel_content, unsafe_allow_html=True)
# =================================================

# To run:
# streamlit run chatbot_frontend.py
# nohup streamlit run chatbot_frontend.py --server.port 8501 > streamlit.log 2>&1 &
