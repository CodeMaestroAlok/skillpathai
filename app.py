import streamlit as st

st.set_page_config(page_title="SkillPath AI", layout="wide")

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "last_intent" not in st.session_state:
    st.session_state.last_intent = None

# ---------------- UI ----------------
st.title("🧠 SkillPath AI")
st.caption("ChatGPT-style Career Guidance Assistant")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask about roadmap, skills, projects, interviews...")

# ---------------- RESPONSE ENGINE ----------------
def generate_response(user_input):
    text = user_input.lower()

    # ---- INTENT DETECTION ----
    if "roadmap" in text:
        st.session_state.last_intent = "roadmap"
        return (
            "### 📍 Data Analyst Roadmap\n"
            "**Beginner:** Excel, SQL, Python basics\n"
            "**Intermediate:** Power BI, statistics, projects\n"
            "**Advanced:** Machine learning, big data, certifications"
        )

    if "project" in text:
        st.session_state.last_intent = "projects"
        return (
            "### 🛠 Real-World Projects\n"
            "1. Sales Dashboard (Power BI)\n"
            "2. E-commerce Data Analysis\n"
            "3. API-based Analytics App"
        )

    if "skill" in text:
        st.session_state.last_intent = "skills"
        return (
            "### 🧩 Required Skills\n"
            "- Python\n"
            "- SQL\n"
            "- Excel\n"
            "- Power BI\n"
            "- Statistics"
        )

    if "interview" in text:
        st.session_state.last_intent = "interview"
        return (
            "### 🎤 Interview Prep\n"
            "- Revise SQL & Python\n"
            "- Practice case studies\n"
            "- Build portfolio projects"
        )

    # ---- FOLLOW-UP HANDLING ----
    if st.session_state.last_intent == "roadmap":
        return (
            "### 🔍 Beginner Phase (Detailed)\n"
            "- Learn Excel formulas\n"
            "- SQL queries (SELECT, JOIN)\n"
            "- Python basics (pandas, numpy)\n"
            "- Build small datasets"
        )

    if st.session_state.last_intent == "projects":
        return (
            "### 📂 Project Tips\n"
            "- Use real datasets\n"
            "- Host on GitHub\n"
            "- Write README & insights"
        )

    # ---- SMART FALLBACK ----
    return (
        "I didn’t fully understand that. You can ask about:\n"
        "- Roadmaps\n"
        "- Skills\n"
        "- Projects\n"
        "- Interview preparation"
    )

# ---------------- PROCESS MESSAGE ----------------
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    response = generate_response(user_input)

    st.session_state.chat.append({"role": "assistant", "content": response})

    st.rerun()
