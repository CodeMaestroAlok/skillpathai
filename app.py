import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.block-container { padding-top: 2rem; }
h1, h2, h3 { color: #f9fafb; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "chat" not in st.session_state:
    st.session_state.chat = [{
        "role": "assistant",
        "content": "Hi 👋 I’m SkillPath AI. Ask me about careers, skills, projects, interviews, or roadmaps!"
    }]

# ---------------- CAREER DATA ----------------
career_data = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP"],
    "Digital Marketer": ["SEO", "Content Writing", "Analytics"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security Basics"],
    "Cloud Engineer": ["AWS", "Docker", "Linux"],
    "Software Tester": ["Manual Testing", "Automation", "Selenium"],
    "UI/UX Designer": ["Figma", "Design Principles", "Prototyping"],
    "Business Analyst": ["Excel", "SQL", "Communication"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes"]
}

project_ideas = {
    "Data Analyst": [
        "Sales Dashboard using Power BI",
        "COVID Data Analysis",
        "E-commerce Analytics"
    ],
    "Web Developer": [
        "Portfolio Website",
        "Blog Platform",
        "E-commerce Website"
    ],
    "AI Engineer": [
        "Chatbot",
        "Resume Screener",
        "Image Classifier"
    ]
}

courses = {
    "Python": "IBM Python for Data Science",
    "SQL": "SQL for Data Analysis – Coursera",
    "Power BI": "Microsoft Power BI Learning Path",
    "Machine Learning": "IBM Machine Learning Professional Certificate",
    "React": "Meta Frontend Developer"
}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 👤 Profile")

    education = st.selectbox(
        "Education Level",
        ["High School", "Diploma", "Undergraduate", "Postgraduate"]
    )

    career = st.selectbox(
        "Target Career",
        list(career_data.keys())
    )

    all_skills = sorted(set(skill for v in career_data.values() for skill in v))
    skills = st.multiselect("Your Skills", all_skills)

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.chat = []
        st.experimental_rerun()

# ---------------- MAIN UI ----------------
st.title("🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

required = career_data[career]
missing = [s for s in required if s not in skills]

# ---------------- SKILL GAP CHART ----------------
df = pd.DataFrame({
    "Skill": required,
    "Status": ["Have" if s in skills else "Missing" for s in required]
})

fig = px.bar(
    df,
    x="Skill",
    color="Status",
    title="📊 Skill Gap Analysis",
    color_discrete_map={"Have": "#22c55e", "Missing": "#ef4444"}
)

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- ROADMAP ----------------
st.markdown("## 🗺️ Career Roadmap")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 Beginner")
    st.write(required[:2])

with col2:
    st.markdown("### 🟡 Intermediate")
    st.write(required[2:4])

with col3:
    st.markdown("### 🔵 Advanced")
    st.write("Certifications, Projects, Real-world Experience")

# ---------------- PROJECT IDEAS ----------------
st.markdown("## 🛠️ Project Ideas")
for p in project_ideas.get(career, []):
    st.write("•", p)

# ---------------- COURSES ----------------
st.markdown("## 🎓 Recommended Courses")
for s in missing:
    if s in courses:
        st.write(f"• **{s}** → {courses[s]}")

# ---------------- CHATBOT ----------------
st.markdown("## 💬 SkillPath AI Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask about jobs, roadmap, projects, interviews...")

if query:
    st.session_state.chat.append({"role": "user", "content": query})

    response = f"""
### 🎯 {career} Guidance

**Your Skills:** {', '.join(skills) if skills else 'None yet'}  
**Skills to Learn:** {', '.join(missing) if missing else 'You are job-ready 🎉'}

#### 📌 Next Steps
- Learn missing skills
- Build 2–3 projects
- Apply for internships / entry roles

Ask me:
• interview questions  
• resume tips  
• career switch advice
"""

    st.session_state.chat.append({"role": "assistant", "content": response})
    st.experimental_rerun()
