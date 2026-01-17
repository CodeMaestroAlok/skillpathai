import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True   # demo login

if "user_email" not in st.session_state:
    st.session_state.user_email = "aloksp135@gmail.com"

if "chat" not in st.session_state:
    st.session_state.chat = []

# --------------------------------------------------
# SIDEBAR – PROFILE
# --------------------------------------------------
with st.sidebar:
    st.title("👤 Profile")
    st.caption(f"Logged in as: **{st.session_state.user_email}**")

    education = st.selectbox(
        "Education Level",
        ["High School", "Undergraduate", "Graduate"]
    )

    career = st.selectbox(
        "Target Career",
        ["Data Analyst", "Web Developer", "AI Engineer"]
    )

    skills = st.multiselect(
        "Your Skills",
        ["Python", "SQL", "Excel", "Power BI", "HTML", "CSS", "JavaScript", "React"]
    )

    if st.button("Logout"):
        st.session_state.chat = []
        st.session_state.logged_in = False
        st.stop()

# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------
st.markdown("## 🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

# --------------------------------------------------
# SKILL GAP ANALYSIS
# --------------------------------------------------
career_skills = {
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning"]
}

required = career_skills.get(career, [])
missing = [s for s in required if s not in skills]

df = pd.DataFrame({
    "Skill": required,
    "Status": ["Have" if s in skills else "Missing" for s in required]
})

if not df.empty:
    fig = px.bar(
        df,
        x="Skill",
        color="Status",
        title="Skill Gap Chart",
        color_discrete_map={"Have": "green", "Missing": "red"}
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# CHAT DISPLAY
# --------------------------------------------------
st.markdown("## 💬 SkillPath AI Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# CHATBOT LOGIC (FIXED)
# --------------------------------------------------
def generate_response(user_text: str) -> str:
    user_text = user_text.lower()

    if "roadmap" in user_text:
        return f"""
### 🛣 Roadmap for **{career}**

**Beginner**
- Learn fundamentals
- Practice basics daily

**Intermediate**
- Build real projects
- Learn tools used in industry

**Advanced**
- Certifications
- Internships
- Open-source contributions
"""

    if "project" in user_text:
        return """
### 🧪 Project Ideas
1. Portfolio website
2. Dashboard using real data
3. API-based mini app
"""

    if "skill" in user_text:
        return f"""
### 📌 Skills Needed for {career}
- {", ".join(required)}
"""

    if "interview" in user_text:
        return """
### 🎤 Interview Prep
- Revise fundamentals
- Practice mock interviews
- Build confidence
"""

    return "I can help with **roadmaps, skills, projects, interviews, and learning plans**. Ask me anything!"

# --------------------------------------------------
# CHAT INPUT (NO RERUN BUG)
# --------------------------------------------------
user_input = st.chat_input("Ask about roadmap, skills, projects, interviews...")

if user_input:
    # Add user message
    st.session_state.chat.append({
        "role": "user",
        "content": user_input
    })

    # Generate response
    response = generate_response(user_input)

    # Add assistant message
    st.session_state.chat.append({
        "role": "assistant",
        "content": response
    })

    # Display immediately (NO rerun)
    with st.chat_message("assistant"):
        st.markdown(response)
