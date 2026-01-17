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
    st.session_state.chat = []

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
if not st.session_state.logged_in:
    st.title("🔐 SkillPath AI Login")
    email = st.text_input("Enter your email")

    if st.button("Login"):
        if email.strip():
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.chat = [{
                "role": "assistant",
                "content": f"Welcome {email}! 👋 Tell me your goal and I’ll guide you step by step."
            }]
            st.rerun()
        else:
            st.error("Please enter a valid email")

    st.stop()

# -------------------------------------------------
# DATA
# -------------------------------------------------
CAREERS = {
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "projects": [
            "Portfolio Website",
            "Todo App (React)",
            "E-commerce Frontend",
            "API-based Dashboard"
        ]
    },
    "Data Analyst": {
        "skills": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
        "projects": [
            "Sales Data Dashboard",
            "COVID Data Analysis",
            "E-commerce Analytics"
        ]
    }
}

COURSES = {
    "HTML": "freeCodeCamp HTML",
    "CSS": "freeCodeCamp CSS",
    "JavaScript": "JavaScript.info",
    "React": "Meta React Certification",
    "Python": "IBM Python for Data Science",
    "SQL": "SQL for Data Analysis – Coursera",
    "Power BI": "Microsoft Power BI Learning Path"
}

# -------------------------------------------------
# CHAT ENGINE (SMARTER)
# -------------------------------------------------
def chat_engine(message, career, skills):
    msg = message.lower()
    required = CAREERS[career]["skills"]
    missing = [s for s in required if s not in skills]

    # ROADMAP
    if "roadmap" in msg or "from scratch" in msg:
        return f"""
### 🗺️ {career} Roadmap

**Step 1 – Basics**
Learn: {', '.join(required[:2])}

**Step 2 – Intermediate**
Learn: {', '.join(required[2:])}

**Step 3 – Projects**
Build real-world projects and deploy them

**Step 4 – Jobs**
Apply for internships and junior roles
"""

    # PROJECT GUIDANCE
    if "project" in msg:
        projects = CAREERS[career]["projects"]
        return f"""
### 🛠️ Recommended Projects for {career}

{chr(10).join([f"• {p}" for p in projects])}

Start with the first one and improve gradually.
"""

    # SKILLS
    if "skill" in msg:
        if missing:
            return f"""
### 📚 Skills You Need to Learn
{', '.join(missing)}

Focus on one skill at a time.
"""
        else:
            return "🎉 You already have the core skills. Focus on projects now."

    # INTERVIEW
    if "interview" in msg:
        return f"""
### 🎯 Interview Preparation for {career}

• Explain your projects clearly  
• Practice coding problems  
• Revise fundamentals  
• Mock interviews
"""

    # JOBS
    if "job" in msg or "salary" in msg:
        return f"{career} roles are in **high demand**. Strong projects + skills = jobs."

    # DEFAULT (SMART)
    return f"""
I understand you're aiming to become a **{career}**.

You can ask me:
• Roadmap from scratch  
• What projects to build  
• Which skills to learn next  
• Interview preparation  
"""

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("👤 Profile")
st.sidebar.write(st.session_state.user_email)

education = st.sidebar.selectbox(
    "Education Level",
    ["High School", "Diploma", "Undergraduate", "Postgraduate"]
)

career = st.sidebar.selectbox(
    "Target Career",
    list(CAREERS.keys())
)

skills = st.sidebar.multiselect(
    "Your Skills",
    CAREERS[career]["skills"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.chat = []
    st.rerun()

# -------------------------------------------------
# MAIN UI
# -------------------------------------------------
st.title("🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

required = CAREERS[career]["skills"]
missing = [s for s in required if s not in skills]

# -------------------------------------------------
# SKILL GAP CHART
# -------------------------------------------------
fig = px.bar(
    x=required,
    y=[1 if s in skills else 0 for s in require]()
