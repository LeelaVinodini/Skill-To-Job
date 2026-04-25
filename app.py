import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="SkillBridge AI", layout="wide")

# =========================
# SKILL DATABASE
# =========================
roles = {
    "Data Analyst": ["python", "sql", "excel", "power bi"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Machine Learning Engineer": ["python", "machine learning", "numpy", "pandas"],
    "Backend Developer": ["python", "django", "api", "database"],
}

# =========================
# MATCH FUNCTION
# =========================
def analyze_skills(user_skills):
    results = []

    for role, skills in roles.items():
        match = len(set(user_skills) & set(skills))
        percent = int((match / len(skills)) * 100)
        missing = list(set(skills) - set(user_skills))

        results.append({
            "Role": role,
            "Match %": percent,
            "Missing Skills": ", ".join(missing)
        })

    return pd.DataFrame(results).sort_values(by="Match %", ascending=False)

# =========================
# ROADMAP FUNCTION
# =========================
def get_roadmap(missing):
    if not missing:
        return "You are job-ready! 🎉"

    roadmap = "👉 Learn in this order:\n"
    for i, skill in enumerate(missing, 1):
        roadmap += f"{i}. {skill}\n"
    return roadmap

# =========================
# UI HEADER
# =========================
st.title("🚀 SkillBridge AI")
st.subheader("Bridge Your Skills to Real Jobs")

# =========================
# INPUT SECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    skill_input = st.text_area("Enter your skills (comma separated)",
                              "python, sql")

with col2:
    resume_input = st.text_area("Paste resume text (optional)")

# =========================
# PROCESS
# =========================
if st.button("Analyze Skills"):
    text = (skill_input + " " + resume_input).lower()
    user_skills = [s.strip() for s in text.split(",")]

    df = analyze_skills(user_skills)

    st.success("Analysis Complete")

    # =========================
    # TOP MATCH
    # =========================
    top_role = df.iloc[0]

    colA, colB, colC = st.columns(3)

    colA.metric("Best Role", top_role["Role"])
    colB.metric("Match %", f"{top_role['Match %']}%")
    colC.metric("Missing Skills", len(top_role["Missing Skills"].split(", ")))

    # =========================
    # TABLE
    # =========================
    st.subheader("📊 All Role Matches")
    st.dataframe(df)

    # =========================
    # ROADMAP
    # =========================
    st.subheader("🧠 Learning Roadmap")
    st.text(get_roadmap(top_role["Missing Skills"].split(", ")))

    # =========================
    # CHART
    # =========================
    st.subheader("📈 Match Visualization")
    st.bar_chart(df.set_index("Role")["Match %"])

# =========================
# FOOTER
# =========================
st.markdown("""
<hr>
<center>Created by <b>Leela Vinodini</b> 💖</center>
""", unsafe_allow_html=True)
