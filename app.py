import streamlit as st
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD SECRETS (SAFE) ----------------
IBM_API_KEY = st.secrets["IBM_API_KEY"]
IBM_PROJECT_ID = st.secrets["IBM_PROJECT_ID"]
IBM_URL = st.secrets["IBM_URL"]

# ---------------- IBM MODEL ----------------
model = Model(
    model_id="ibm/granite-13b-chat-v2",
    credentials={
        "apikey": IBM_API_KEY,
        "url": IBM_URL
    },
    project_id=IBM_PROJECT_ID,
    params={
        GenParams.MAX_NEW_TOKENS: 450,
        GenParams.TEMPERATURE: 0.3,
        GenParams.TOP_P: 0.9
    }
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("👤 User Profile")

education = st.sidebar.selectbox(
    "Education Level",
    ["High School", "Diploma", "Undergraduate", "Postgraduate"]
)

career = st.sidebar.selectbox(
    "Target Career",
    [
        "Data Analyst",
        "Web Developer",
        "AI Engineer",
        "Cybersecurity",
        "Software Engineer"
    ]
)

skills = st.sidebar.multiselect(
    "Current Skills",
    [
        "Python", "SQL", "Excel", "Statistics",
        "HTML", "CSS", "JavaScript",
        "Machine Learning", "Git"
    ]
)

experience = st.sidebar.slider("Experience (Years)", 0, 10, 0)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- MAIN UI ----------------
st.title("🤖 SkillPath AI")
st.caption("Career Guidance Chatbot powered by IBM Watsonx (Tokyo Region)")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input(
    "Ask about career guidance, roadmap, resume tips, projects..."
)

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
You are SkillPath AI, a professional career guidance assistant.

User Profile:
Education: {education}
Career Goal: {career}
Skills: {", ".join(skills) if skills else "None"}
Experience: {experience} years

User Question:
{user_input}

Include:
1. Career guidance
2. Skill gap analysis
3. Learning roadmap
4. Weekly plan
5. Resume tips
6. Career readiness score (0–100)
7. 3 project ideas
"""

    try:
        response = model.generate_text(prompt)
    except Exception:
        response = (
            "⚠️ IBM Watsonx service is temporarily unavailable.\n"
            "Please try again later."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)

# ---------------- CHAT EXPORT ----------------
if st.session_state.messages:
    chat_log = ""
    for m in st.session_state.messages:
        role = "User" if m["role"] == "user" else "SkillPath AI"
        chat_log += f"{role}: {m['content']}\n\n"

    st.download_button(
        "📄 Download Chat History",
        chat_log,
        "skillpath_chat.txt",
        "text/plain"
    )
