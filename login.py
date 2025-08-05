import streamlit as st
from credentials import users  # credentials

def login():
    st.title("Login to CivicMind")
    st.write("Use the ID and password shared by the App Inventor Foundation to access the CivicMind platform. \n"
        "Please fill the participant survey to receive your ID and password.")

    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

    if submit_button:
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.success("Login successful! Redirecting...")
            st.rerun() # there is no experimental_rerun
        else:
            st.error("Invalid username or password. Please try again.")
    
    # Important: Stop further execution
    return


# def login():
#     if st.session_state.get("authenticated"):
#         st.write("Already logged in.")
#         return

#     st.title("Login to CivicMind")
#     st.write("Use the key and password shared by the App Inventor Foundation")

#     with st.form(key="login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submit_button = st.form_submit_button(label="Login")

#     if submit_button:
#         if username in users and users[username] == password:
#             st.session_state["authenticated"] = True
#             st.success("Login successful! Redirecting...")
#             # st.experimental_rerun()
#         else:
#             st.error("Invalid username or password. Please try again.")
    
#     return



def logout():
    st.session_state["authenticated"] = False
    st.experimental_rerun()

# # Initialize session state if not already set
# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False

# if not st.session_state["authenticated"]:
#     login()
# else:
#     st.write("You are logged in!")
#     if st.button("Logout", key="logout_button"):
#         logout()
