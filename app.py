import streamlit as st
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "chat" not in st.session_state:
    st.session_state.chat = [
        {
            "role": "assistant",
            "content": "Hi 👋 I’m SkillPath AI. Ask me about careers, skills, roadmaps, projects, or interviews!"
        }
    ]

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
if not st.session_state.logged_in:
    st.title("🔐 SkillPath AI Login")
    st.caption("Simple email-based login (demo-safe & cloud-stable)")

    email = st.text_input("📧 Enter your email")

    if st.button("Login"):
        if email.strip() == "":
            st.error("Please enter a valid email")
        else:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.chat = [
                {
                    "role": "assistant",
                    "content": f"Welcome {email}! 👋 I’m SkillPath AI."
                }
            ]
            st.rerun()

    st.stop()

# -------------------------------------------------
# DATA
# -------------------------------------------------
CAREER_DATA = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning"],
    "Digital Marketer": ["SEO", "Content Writing", "Analytics"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security Basics"]
}

COURSES = {
    "Python": "IBM Python for Data Science",
    "SQL": "SQL for Data Analysis (Coursera)",
    "Power BI": "Microsoft Power BI Learning Path",
    "Machine Learning": "IBM Machine Learning Certificate",
    "React": "Meta Frontend Developer"
}

# -------------------------------------------------
# CHAT ENGINE (FAST)
# -------------------------------------------------
def generate_response(text, career, missing_skills):
    t = text.lower()

    if "roadmap" in t:
        return f"""
### 🗺️ Roadmap to become a **{career}**
**Beginner:** Learn fundamentals  
**Intermediate:** Build projects  
**Advanced:** Certifications & real-world experience
"""

    if "skill" in t:
        if missing_skills:
            return f"You should focus on learning: **{', '.join(missing_skills)}**."
        return "🎉 You already have all the core skills!"

    if "project" in t:
        return "Build 2–3 real-world projects and publish them on GitHub."

    if "job" in t or "salary" in t:
        return f"{career} roles are in **high demand**. Focus on skills + internships."

    if "interview" in t:
        return "Practice SQL/Python questions, explain projects clearly, and revise fundamentals."

    return "I can help with career paths, skills, projects, interviews, and learning plans."

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("👤 Profile")
st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_email}")

education = st.sidebar.selectbox(
    "Education Level",
    ["High School", "Diploma", "Undergraduate", "Postgraduate"]
)

career = st.sidebar.selectbox(
    "Target Career",
    list(CAREER_DATA.keys())
)

skills = st.sidebar.multiselect(
    "Your Skills",
    CAREER_DATA[career]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.chat = []
    st.rerun()

# -------------------------------------------------
# MAIN UI
# -------------------------------------------------
st.title("🧠 SkillPath AI")
st.caption("Fast, ChatGPT-style Career Guidance Assistant")

required_skills = CAREER_DATA[career]
missing = [s for s in required_skills if s not in skills]

# -------------------------------------------------
# SKILL GAP CHART
# -------------------------------------------------
st.subheader("📊 Skill Gap Analysis")

chart_data = {
    "Skill": required_skills,
    "Status": ["Have" if s in skills else "Missing" for s in required_skills]
}

fig = px.bar(
    chart_data,
    x="Skill",
    color="Status",
    color_discrete_map={"Have": "green", "Missing": "red"},
    title="Skill Gap Chart"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# ROADMAP
# -------------------------------------------------
st.subheader("🛣 Career Roadmap")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 Beginner")
    st.write(required_skills[:2])

with col2:
    st.markdown("### 🟡 Intermediate")
    st.write(required_skills[2:4])

with col3:
    st.markdown("### 🔵 Advanced")
    st.write("Projects, certifications, specialization")

# -------------------------------------------------
# COURSES
# -------------------------------------------------
st.subheader("🎓 Recommended Courses")

for s in missing:
    if s in COURSES:
        st.write(f"• **{s}** → {COURSES[s]}")

# -------------------------------------------------
# CHAT UI (FAST)
# -------------------------------------------------
st.subheader("💬 SkillPath AI Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about roadmap, skills, projects, interviews...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    reply = generate_response(user_input, career, missing)

    st.session_state.chat.append({"role": "assistant", "content": reply})
