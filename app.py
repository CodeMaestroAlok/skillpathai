import streamlit as st
import plotly.express as px

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.logged_in:
    st.set_page_config(page_title="SkillPath AI Login", layout="centered")

    st.title("🔐 SkillPath AI Login")
    st.markdown("Simple & secure email-based login")

    email = st.text_input("📧 Enter your email")

    if st.button("Login"):
        if email.strip() == "":
            st.error("Please enter a valid email")
        else:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.chat = []
            st.success("Login successful!")
            st.rerun()

    st.stop()

# -----------------------------
# MAIN APP
# -----------------------------
st.set_page_config(page_title="SkillPath AI", layout="wide")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("👤 Profile")
st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_email}")

education = st.sidebar.selectbox(
    "Education Level",
    ["High School", "Diploma", "Undergraduate", "Postgraduate"]
)

career = st.sidebar.selectbox(
    "Target Career",
    ["Data Analyst", "Data Scientist", "Web Developer", "AI Engineer"]
)

skills = st.sidebar.multiselect(
    "Your Skills",
    ["Python", "SQL", "Excel", "Statistics", "Power BI"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.chat = []
    st.rerun()

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

# -----------------------------
# SKILL GAP ANALYSIS
# -----------------------------
st.subheader("📊 Skill Gap Analysis")

career_skills = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Data Scientist": ["Python", "Statistics", "SQL", "Machine Learning"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Python"],
    "AI Engineer": ["Python", "Deep Learning", "Maths"]
}

required = career_skills.get(career, [])
missing = [s for s in required if s not in skills]

chart_data = []
for s in required:
    chart_data.append({
        "Skill": s,
        "Status": "Have" if s in skills else "Missing"
    })

fig = px.bar(
    chart_data,
    x="Skill",
    color="Status",
    title="Skill Gap Chart",
    color_discrete_map={"Have": "green", "Missing": "red"}
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# CAREER ROADMAP
# -----------------------------
st.subheader("🛣 Career Roadmap")

st.markdown("### 🟢 Beginner")
st.write(["Python", "SQL"])

st.markdown("### 🟡 Intermediate")
st.write(["Excel", "Power BI"])

st.markdown("### 🔵 Advanced")
st.write("Specialization, certifications, real-world projects")

# -----------------------------
# COURSES
# -----------------------------
st.subheader("🎓 Recommended Courses")

course_map = {
    "Python": "IBM Python for Data Science",
    "SQL": "SQL for Data Analysis – Coursera",
    "Excel": "Excel for Data Analysis",
    "Power BI": "Microsoft Power BI Learning Path",
    "Statistics": "Statistics for Data Science"
}

for s in missing:
    if s in course_map:
        st.write(f"• **{s}** → {course_map[s]}")

# -----------------------------
# CHATBOT
# -----------------------------
st.subheader("💬 SkillPath AI Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about careers, skills, roadmap, interviews...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    # Simple intelligent responses
    if "roadmap" in user_input.lower():
        response = f"To become a {career}, start with {', '.join(required[:2])}, then move to advanced tools."
    elif "skill" in user_input.lower():
        response = f"You should focus on learning: {', '.join(missing) if missing else 'No missing skills!'}"
    elif "job" in user_input.lower():
        response = f"{career} roles are in high demand. Build projects and apply for internships."
    else:
        response = "I can help you with career paths, skills, projects, and interview preparation."

    st.session_state.chat.append({"role": "assistant", "content": response})
