import streamlit as st
import chatbot_backend as demo
import login

# ============= LOG IN ===================================
# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # <- bypass login for now

# # If user is not authenticated, show login page
# if not st.session_state["authenticated"]:
#     login.login()
#     st.stop()  # Stop execution here if not authenticated
# ========================================================

# 1 Logo
st.image("logo.png", width=350)

# 2 Title
st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>App Inventor Assistant 🤖🧱</h1>",
    unsafe_allow_html=True
)

# 3 Sidebar
with st.sidebar:
    st.header("Settings ⚙️")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.referred_doc = None
        st.session_state.doc_open = False
        st.success("Chat history cleared!")

    # if st.button("Logout"):
    #     login.logout

# 4 Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "referred_doc" not in st.session_state:
    st.session_state.referred_doc = None
if "doc_open" not in st.session_state:
    st.session_state.doc_open = False

# 5 Custom CSS for the Sliding Panel
st.markdown("""
<style>
/* Container for the referred document */
#referred-doc {
    position: fixed;
    top: 80px; /* Adjust if you have a header or offset at the top */
    right: 0;
    width: 400px;
    height: calc(100% - 80px);
    background-color: #F5F5F5;
    border-left: 1px solid #CCC;
    padding: 1rem;
    box-shadow: -3px 0 5px rgba(0,0,0,0.1);
    transform: translateX(100%);        /* Hidden by default */
    transition: transform 0.3s ease-in-out;
    overflow-y: auto;
    z-index: 9999; /* Ensure it appears on top of other elements */
}
/* When we add the "open" class, the panel slides into view */
#referred-doc.open {
    transform: translateX(0);
}
</style>
""", unsafe_allow_html=True)

# 6 Display Existing Chat
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(f"**{msg['role'].capitalize()}:** {msg['text']}")

# 7 Chat Input
input_text = st.chat_input("💬 Ask me ...")
if input_text:
    # Display user message
    st.chat_message("user").markdown(input_text)
    st.session_state.chat_history.append({'role': 'user', 'text': input_text})

    # Call your backend to get the response
    chat_response = demo.demo_conversation(input_text)

    # 8 Parse out the main response vs. referred document
    if "**Referred Document**:" in chat_response:
        main_response, referred_doc = chat_response.split("**Referred Document**:")
        main_response = main_response.strip()
        referred_doc = referred_doc.strip()
    else:
        main_response = chat_response
        referred_doc = None

    # Display assistant message
    st.chat_message("assistant").markdown(main_response)
    st.session_state.chat_history.append({"role": "assistant", "text": main_response})
    st.session_state.referred_doc = referred_doc

# 9 Toggle Button for the Slide Panel
# Only show the toggle button if there's a valid doc to show
if st.session_state.referred_doc and st.session_state.referred_doc != "No document was searched":
    if st.button("Open/Close Referred Document"):
        st.session_state.doc_open = not st.session_state.doc_open

# 10 The Sliding Panel on the Right
doc_container_class = "open" if st.session_state.doc_open else ""
doc_content = st.session_state.referred_doc if st.session_state.referred_doc else "No referred document"

# We place the referred doc inside a fixed-positioned <div>
st.markdown(
    f'<div id="referred-doc" class="{doc_container_class}">{doc_content}</div>',
    unsafe_allow_html=True
)


# # # run
# # # streamlit run chatbot_frontend.py
# # # nohup streamlit run chatbot_frontend.py --server.port 8501 > streamlit.log 2>&1 &

## Deploy on AWS EC2
