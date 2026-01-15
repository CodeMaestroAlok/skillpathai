import streamlit as st
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- DATA ----------------
CAREERS = {
    "Data Analyst": {
        "skills": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
        "demand": "High",
        "description": "Analyze data to support business decisions.",
        "courses": {
            "Python": "IBM Python for Data Science",
            "SQL": "SQL for Data Analysis (Coursera)",
            "Power BI": "Microsoft Power BI Learning Path"
        }
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "demand": "High",
        "description": "Build and maintain websites and web apps.",
        "courses": {
            "JavaScript": "JavaScript Basics (Udemy)",
            "React": "React Official Docs"
        }
    },
    "AI Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning"],
        "demand": "Medium",
        "description": "Design and deploy AI models.",
        "courses": {
            "ML": "Andrew Ng ML Course",
            "DL": "Deep Learning Specialization"
        }
    }
}

EDUCATION_LEVELS = ["High School", "Diploma", "Bachelor", "Master"]

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("👤 Profile")

education = st.sidebar.selectbox("Education Level", EDUCATION_LEVELS)
career = st.sidebar.selectbox("Target Career", list(CAREERS.keys()))
user_skills = st.sidebar.multiselect(
    "Your Skills",
    CAREERS[career]["skills"]
)

if st.sidebar.button("Logout"):
    st.session_state.chat = []
    st.experimental_set_query_params()

# ---------------- MAIN UI ----------------
st.title("🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

# ---------------- SKILL GAP ----------------
required_skills = CAREERS[career]["skills"]
missing_skills = [s for s in required_skills if s not in user_skills]

st.subheader("📊 Skill Gap Analysis")

chart_data = {
    "Skill": required_skills,
    "Status": ["Have" if s in user_skills else "Missing" for s in required_skills]
}

fig = px.bar(
    chart_data,
    x="Skill",
    color="Status",
    title="Skill Gap Chart"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- CAREER ROADMAP ----------------
st.subheader("🗺️ Career Roadmap")

st.markdown("### 🟢 Beginner")
st.write(missing_skills[:2] if missing_skills else "You are job-ready!")

st.markdown("### 🟡 Intermediate")
st.write(missing_skills[2:4])

st.markdown("### 🔵 Advanced")
st.write("Projects, certifications, real-world experience")

# ---------------- COURSES ----------------
st.subheader("🎓 Recommended Courses")
for skill, course in CAREERS[career]["courses"].items():
    st.write(f"• **{skill}** → {course}")

# ---------------- CHATBOT ----------------
st.subheader("💬 SkillPath AI Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about careers, skills, roadmap, jobs...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})

    response = f"""
**Career:** {career}  
**Demand Level:** {CAREERS[career]['demand']}

Based on your education ({education}) and skills, here’s guidance:

• Focus on learning: {', '.join(missing_skills) if missing_skills else 'Advanced projects'}
• Build 2–3 portfolio projects  
• Apply for internships and entry-level roles  

Ask me for:
✔ Resume tips  
✔ Interview questions  
✔ Project ideas  
✔ Career switching advice
"""

    st.session_state.chat.append({"role": "assistant", "content": response})
