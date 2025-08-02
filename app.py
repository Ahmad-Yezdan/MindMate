import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()


# ---- API Setup ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # for local use
GROQ_API_KEY = st.secrets["API"]["GROQ_API_KEY"]  # for deployment use
MODEL = "llama3-8b-8192"  

def get_groq_response(system_prompt, user_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# ---- Streamlit UI ----
st.set_page_config(page_title="MindMate – Youth Mental Health", page_icon="💙")

st.sidebar.title("🧭 MindMate")
page = st.sidebar.radio("Navigate", ["🤖 AI Chatbot", "📓 Journal"])

# ---- Common Sidebar Controls ----
if page == "🤖 AI Chatbot":
    st.title("🤖 MindMate – AI Mental Health Assistant")
    st.markdown("Talk about anything that's on your mind. I'm here to support you. 💙")
    
    tone = st.selectbox("Choose the tone you'd like me to use:", ["Friendly", "Motivational", "Supportive"])
    topic = st.selectbox("What are you facing right now?", ["Stress", "Anxiety", "Exam Pressure", "Loneliness", "Other"])
    
    user_input = st.text_input("Your message")

    def is_dangerous(text):
        red_flags = ["suicide", "kill myself", "end my life", "cut myself", "worthless"]
        return any(flag in text.lower() for flag in red_flags)

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a message.")
        elif is_dangerous(user_input):
            st.error("⚠️ You may be going through something serious. Please talk to a trusted adult or professional. You're not alone. ❤️")
        else:
            with st.spinner("Thinking..."):
                system_prompt = (
                    f"You are a {tone.lower()} mental health assistant for teenagers. "
                    f"Speak kindly and provide support specifically about {topic.lower()}."
                )
                response = get_groq_response(system_prompt, user_input)
            st.success("Here's what I think:")
            st.markdown(response)
    
    st.caption("🚨 *This chatbot is not a replacement for professional help.*")

# ---- Journal Page ----
else:
    st.title("📓 My Private Journal")
    st.markdown("Write down your thoughts and feelings. This stays private and can help clear your mind.")
    
    journal_entry = st.text_area("Write here", height=200)
    
    if st.button("Save Entry"):
        if journal_entry.strip():
            with open("journal.txt", "a", encoding="utf-8") as f:
                f.write(f"\n---\n{journal_entry}\n")
            st.success("Saved to local journal.txt 📄")
        else:
            st.warning("Please write something before saving.")

    st.caption("🧠 Writing your thoughts can be a powerful mental health tool.")

