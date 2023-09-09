import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def main():
    st.title("Broom Finder")
    with open("css/chat.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        chat_history = []
        st.session_state.chat_history = chat_history

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    st.text_input("Your Question", key="user_input")
    st.button("Ask", type="primary", on_click=handle_enter)


def handle_enter():
    value = st.session_state.user_input.strip()
    bot_response = generate_bot_response(value)
    st.session_state.chat_history.append({"sender": "User", "message": value})
    st.session_state.chat_history.append({"sender": "Bot", "message": bot_response})
    display_mssage(st.session_state.chat_history)
    st.session_state.user_input = ""
    
@st.cache_resource
def get_query_engine():
    from llama_index_bot import load_index
    return load_index()
   
def generate_bot_response(user_input):
    print(f"input: {user_input}")
    query_engine=get_query_engine()
    response = query_engine.chat(user_input)
    print(response.response)
    return response.response

def display_mssage(chat_history):
    for chat in chat_history:
        if chat["sender"] == "User":
            with st.container():
                col1, col2 = st.columns([1, 11])
                col1.image("resources/user_icon.jfif", width=30)
                # col1.markdown("<div class='user-label'>User</div>", unsafe_allow_html=True)
                col2.markdown(
                    f"<div class='user-message'>{chat['message']}</div>",
                    unsafe_allow_html=True
                )
        else:
            with st.container():
                col1, col2 = st.columns([1, 11])
                # col1.markdown("<div class='bot-label'>Bot</div>", unsafe_allow_html=True)
                col1.image("resources/bot_icon.jfif", width=30)
                col2.markdown(
                    f"<div class='bot-message'>{chat['message']}</div>",
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
