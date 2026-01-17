import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# ------------------ DATABASE ------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
)
""")
conn.commit()

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

# ------------------ LOGIN ------------------
def login():
    st.title("🔐 Login to SkillPath AI")

    email = st.text_input("Email")

    if st.button("Login / Sign Up"):
        if not email:
            st.error("Please enter an email")
            return

        c.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
        conn.commit()

        st.session_state.logged_in = True
        st.session_state.email = email
        st.success("Logged in successfully!")
        st.rerun()

# ------------------ LOGOUT ------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.chat = []
    st.rerun()

# ------------------ DATA ------------------
career_skills = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "AI Engineer": ["Python", "ML", "Deep Learning", "Math", "NLP"]
}

career_roadmap = {
    "Beginner": ["Python", "SQL"],
    "Intermediate": ["Excel", "Power BI"],
    "Advanced": ["Projects", "Certifications", "Internships"]
}

# ------------------ CHATBOT ------------------
def chatbot_reply(prompt, career):
    time.sleep(0.5)  # improves UX, avoids spam replies

    if "project" in prompt.lower():
        return f"Build 2–3 real-world {career} projects and publish them on GitHub."

    if "skills" in prompt.lower():
        return f"Focus on mastering core {career} skills step by step."

    if "interview" in prompt.lower():
        return "Practice problem-solving, mock interviews, and real-world scenarios."

    return "I can help with career paths, skills, projects, interviews, and learning plans."

# ------------------ MAIN APP ------------------
def app():
    st.sidebar.title("👤 Profile")
    st.sidebar.write(f"Logged in as: **{st.session_state.email}**")

    education = st.sidebar.selectbox(
        "Education Level",
        ["High School", "Undergraduate", "Postgraduate"]
    )

    career = st.sidebar.selectbox(
        "Target Career",
        list(career_skills.keys())
    )

    user_skills = st.sidebar.multiselect(
        "Your Skills",
        career_skills[career]
    )

    if st.sidebar.button("Logout"):
        logout()

    st.title("🧠 SkillPath AI")
    st.caption("ChatGPT-style Career Guidance Assistant")

    # ------------------ SKILL GAP ------------------
    required = career_skills[career]
    missing = [s for s in required if s not in user_skills]

    df = pd.DataFrame({
        "Skill": required,
        "Status": ["Missing" if s in missing else "Available" for s in required],
        "Count": [1] * len(required)
    })

    st.subheader("📊 Skill Gap Analysis")

    fig = px.bar(
        df,
        x="Skill",
        y="Count",
        color="Status",
        color_discrete_map={
            "Missing": "#ff4b4b",
            "Available": "#2ecc71"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------ ROADMAP ------------------
    st.subheader("🛣 Career Roadmap")
    for level, skills in career_roadmap.items():
        st.markdown(f"**{level}**")
        st.write(", ".join(skills))

    # ------------------ CHAT ------------------
    st.subheader("💬 SkillPath AI Chat")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about roadmap, skills, projects, interviews...")

    if user_input:
        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        reply = chatbot_reply(user_input, career)

        st.session_state.chat.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

# ------------------ ROUTING ------------------
if not st.session_state.logged_in:
    login()
else:
    app()
