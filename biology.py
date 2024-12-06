import streamlit as st
import openai

# Function to get a response from ChatGPT
def get_chatgpt_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly knowledgeable and friendly assistant specializing in biology. "
                        "You can answer questions about topics like cells, photosynthesis, genetics, and ecology. "
                        "For non-biology questions, politely reply: 'Sorry, I am a BIOLOGY chatbot, and I can't answer other questions.' "
                        "Provide detailed and accurate information concisely and clearly."
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

image = 'https://radical.vc/wp-content/uploads/2023/07/Biology-Image.jpg'
   # CSS orqali orqa fon sozlash
st.markdown(
    f"""
    <style>
    /* Tana uchun umumiy fon */
    body {{
        background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url('{image}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    /* Asosiy ilova o'rnatmalarini o'zgartirish */
 .stApp {{
     background: rgba(255, 255, 255, 0.85);
     padding: 2rem;
     border-radius: 15px;
     box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
     max-width: 900px;
     margin: 2rem auto;
     animation: fadeIn 2s ease-in-out;
 }}
    /* Tugmalar uchun animatsiya */
    button {{
        background-color: #007BFF;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        border-radius: 5px;
        transition: transform 0.3s ease, background-color 0.3s ease;
    }}
    button:hover {{
        background-color: #0056b3;
        transform: scale(1.05);
    }}
    /* Matn uchun animatsiyalar */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}
    h1, h2, h3 {{
        font-family: 'Helvetica', sans-serif;
        animation: fadeIn 2s ease-in-out;
    }}
    .assistant-message em {{
        color: #007BFF;
        font-style: italic;
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{
        0% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.6; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# Page 1: API Key Entry
def api_key_page():
    
    st.title("🔑 Welcome to the Biology Chatbot!")
    st.write("Please enter your OpenAI API Key to proceed.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Input for API key
    api_key = st.text_input("OpenAI API Key:", type="password")

    if st.button("Submit"):
        if api_key.strip():
            openai.api_key = api_key
            st.session_state.api_key = api_key
            st.session_state.current_page = "chatbot"

# Page 2: Chatbot Interface
def chatbot_page():
    st.title("🌿 Biology Chatbot")
    st.write("Ask me anything about biology!")

    # Chat history stored in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input for user question
    user_question = st.text_input("Your question:", "", key="input_box")

    # Detect Enter key press and Send button
    if st.button("Send") or st.session_state.get("enter_pressed", False):
        if user_question.strip():
            with st.spinner("Thinking..."):
                try:
                    answer = get_chatgpt_response(user_question)
                    # Append to chat history
                    st.session_state.chat_history.insert(0, {"role": "user", "content": user_question})
                    st.session_state.chat_history.insert(0, {"role": "assistant", "content": answer})
                    st.session_state["enter_pressed"] = False
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # JavaScript to detect Enter key
    st.markdown(
        """
        <script>
        document.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                window.parent.document.querySelector("button[title='Send']").click();
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
                <div style="background-color:#E0F7FA; padding:10px; border-radius:10px; margin-bottom:10px;">
                    <b>You:</b> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"""
                <div style="background-color:#F1F8E9; padding:10px; border-radius:10px; margin-bottom:10px;">
                    <b>Biology Bot:</b> {message["content"]}
                </div>
            """, unsafe_allow_html=True)

    # Button to reset API Key (go back to the first page)
    if st.button("🔄 Reset API Key"):
        st.session_state.api_key = None
        st.session_state.current_page = "api_key"

# Main Function: Route Pages
def main():
    # Initialize the session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "api_key"

    # Page routing based on session state
    if st.session_state.current_page == "chatbot" and "api_key" in st.session_state:
        chatbot_page()
    else:
        api_key_page()

if __name__ == "__main__":
    main()
