import streamlit as st
from groq import Groq

# 1. Page Configuration (Sets up the web page look)
st.set_page_config(page_title="IXITRI-Ai", page_icon="🤖", layout="centered")
st.title("Welcom, IXITRI-Ai At you Service")
st.caption("Powered by OJANA")

# 2. Initialize Groq Client
client = Groq(api_key="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")

# 3. Define the Core Instructions (Allows general chat, enforces Creator & IXITRI Rules)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful and intelligent AI assistant. You can chat with the user about "
        "any topic, answer general questions, or assist with their requests naturally.\n\n"
        
        "CRITICAL CREATOR RULE:\n"
        "If anyone asks who created you, who built you, or who your developer is, you must reply exactly with: "
        "'I was created by OJANA. His Instagram is @on_abdelilah, and he is an AI developer. Right now, "
        "he is working on a big project called IXITRI-Connect.'\n\n"
        
        "IXITRI MEANING RULE:\n"
        "If anyone asks what 'IXITRI' means, you must explain that it means 'The immortal star'. "
        "Break it down for them exactly like this:\n"
        "- 'IX' is the Roman numeral for 9.\n"
        "- 'ITRI' means 'star' in the Amazigh language.\n"
        "Together, it gives the powerful meaning of 'The immortal star'."
    )
}

# 4. Initialize Chat History in Session State
if "messages" not in st.session_state:
    # Inject the system instructions at the very beginning of the memory loop
    st.session_state.messages = [SYSTEM_PROMPT]

# 5. Display past chat messages on the screen (Hiding the system prompt from the user UI)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Handle New User Input (The ChatGPT-style typing bar)
if user_input := st.chat_input("Ask me anything..."):
    
    # Display user message instantly on the web screen
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Groq API with full conversation history
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages  # Sends system rules + chat history
        )
        
        reply = response.choices[0].message.content
        message_placeholder.markdown(reply)
        
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": reply})