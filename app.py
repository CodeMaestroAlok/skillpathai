import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🧠",
    layout="wide"
)

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    phone TEXT,
    provider TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user_id INTEGER,
    role TEXT,
    message TEXT
)
""")
conn.commit()

# ================= CAREER DATA =================
CAREERS = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security", "Python"],
    "Cloud Engineer": ["AWS", "Azure", "Linux", "Networking"],
    "Digital Marketer": ["SEO", "Content Writing", "Analytics"],
    "UI/UX Designer": ["Figma", "Design Thinking", "Wireframing"],
    "Mobile App Developer": ["Flutter", "React Native", "APIs"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD"],
    "Business Analyst": ["Excel", "SQL", "Visualization"]
}

EDUCATION_LEVELS = ["High School", "Diploma", "Undergraduate", "Postgraduate"]

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= AUTH =================
def login_user(email=None, phone=None, provider="email"):
    cursor.execute(
        "INSERT INTO users (email, phone, provider) VALUES (?,?,?)",
        (email, phone, provider)
    )
    conn.commit()
    return cursor.lastrowid

def get_user(email=None, phone=None):
    if email:
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    else:
        cursor.execute("SELECT id FROM users WHERE phone=?", (phone,))
    row = cursor.fetchone()
    return row[0] if row else None

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:
    st.title("🔐 SkillPath AI Login")

    tab1, tab2, tab3 = st.tabs(["📧 Email", "📱 Phone", "🌐 Google"])

    with tab1:
        email = st.text_input("Email")
        if st.button("Login with Email"):
            uid = get_user(email=email)
            if not uid:
                uid = login_user(email=email)
            st.session_state.logged_in = True
            st.session_state.user_id = uid
            st.rerun()

    with tab2:
        phone = st.text_input("Phone Number")
        if st.button("Login with Phone"):
            uid = get_user(phone=phone)
            if not uid:
                uid = login_user(phone=phone, provider="phone")
            st.session_state.logged_in = True
            st.session_state.user_id = uid
            st.rerun()

    with tab3:
        google = st.text_input("Google Email")
        if st.button("Continue with Google"):
            uid = get_user(email=google)
            if not uid:
                uid = login_user(email=google, provider="google")
            st.session_state.logged_in = True
            st.session_state.user_id = uid
            st.rerun()

# ================= DASHBOARD =================
else:
    st.title("🧠 SkillPath AI")
    st.caption("ChatGPT-style Career Guidance Assistant")

    # -------- SIDEBAR --------
    st.sidebar.header("👤 Profile")

    education = st.sidebar.selectbox("Education Level", EDUCATION_LEVELS)
    career = st.sidebar.selectbox("Target Career", list(CAREERS.keys()))
    skills = st.sidebar.multiselect("Your Skills", CAREERS[career])

    # -------- SKILL GAP --------
    required = CAREERS[career]
    missing = list(set(required) - set(skills))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📉 Skill Gap Analysis")
        df = pd.DataFrame({
            "Skill": required,
            "Status": ["Have" if s in skills else "Missing" for s in required]
        })
        fig = px.bar(
            df,
            x="Skill",
            color="Status",
            title="Skill Gap Chart",
            color_discrete_map={"Have": "green", "Missing": "red"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🛣 Career Roadmap")

        st.markdown("### 🟢 Beginner")
        st.write(missing[:2] or "Focus on fundamentals")

        st.markdown("### 🟡 Intermediate")
        st.write(missing[2:4] or "Build projects")

        st.markdown("### 🔵 Advanced")
        st.write("Specialization, certifications, real-world projects")

    # -------- CHATBOT --------
    st.subheader("💬 SkillPath AI Chat")

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask about roadmap, skills, jobs...")

    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})

        response = f"""
Here is a clear roadmap for **{career}** based on your profile:

🎓 Education: {education}

✅ Skills you have:
{', '.join(skills) if skills else 'None yet'}

❌ Skills to learn:
{', '.join(missing) if missing else 'You are job-ready!'}

📌 Next Steps:
• Learn missing skills step-by-step
• Build 2–3 projects
• Apply for internships or entry-level roles
"""

        st.session_state.chat.append({"role": "assistant", "content": response})
        st.rerun()

    # -------- LOGOUT --------
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.chat = []
        st.rerun()

