import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="SkillBridge AI", layout="wide")

# =========================
# EXTENDED ROLE DATABASE
# =========================
roles = {
    "Frontend Developer": ["html", "css", "javascript", "react", "bootstrap"],
    "Backend Developer": ["python", "django", "flask", "api", "database"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node", "mongodb"],
    "Data Analyst": ["python", "sql", "excel", "power bi", "tableau"],
    "Data Scientist": ["python", "machine learning", "statistics", "pandas", "numpy"],
    "Machine Learning Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"],
    "AI Engineer": ["python", "nlp", "deep learning", "transformers", "llm"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "ci/cd", "linux"],
    "Cloud Engineer": ["aws", "azure", "gcp", "cloud computing", "networking"],
    "Cybersecurity Analyst": ["network security", "cryptography", "ethical hacking", "firewalls"],
    "Mobile App Developer": ["flutter", "android", "kotlin", "swift", "react native"],
    "Game Developer": ["unity", "c#", "unreal engine", "game physics"],
    "Database Administrator": ["sql", "oracle", "mysql", "database tuning"],
    "Software Tester (QA)": ["manual testing", "automation testing", "selenium", "jira"],
    "UI/UX Designer": ["figma", "adobe xd", "wireframing", "prototyping"],
    "Blockchain Developer": ["solidity", "web3", "ethereum", "smart contracts"],
    "Embedded Systems Engineer": ["c", "microcontrollers", "iot", "arduino"],
    "Site Reliability Engineer": ["linux", "monitoring", "aws", "scripting"],
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
            "Matched Skills": match,
            "Missing Skills": ", ".join(missing)
        })

    return pd.DataFrame(results).sort_values(by="Match %", ascending=False)

# =========================
# ROADMAP FUNCTION
# =========================
def get_roadmap(missing):
    if not missing or missing == ['']:
        return "You are job-ready! 🎉"

    roadmap = ""
    for i, skill in enumerate(missing, 1):
        roadmap += f"{i}. {skill}\n"
    return roadmap

# =========================
# UI HEADER
# =========================
st.title("🚀 SkillBridge AI")
st.subheader("Find Your Perfect Role in IT Industry")

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    skill_input = st.text_area("Enter your skills (comma separated)",
                              "python, sql, html")

with col2:
    resume_input = st.text_area("Paste resume text (optional)")

# =========================
# PROCESS
# =========================
if st.button("Analyze Skills"):
    text = (skill_input + " " + resume_input).lower()
    user_skills = [s.strip() for s in text.replace("\n", ",").split(",") if s.strip()]

    df = analyze_skills(user_skills)

    st.success("Analysis Complete ✅")

    top_role = df.iloc[0]

    colA, colB, colC = st.columns(3)
    colA.metric("Best Role", top_role["Role"])
    colB.metric("Match %", f"{top_role['Match %']}%")
    colC.metric("Skills Matched", top_role["Matched Skills"])

    # =========================
    # TABLE
    # =========================
    st.subheader("📊 All Role Matches")
    st.dataframe(df)

    # =========================
    # ROADMAP
    # =========================
    st.subheader("🧠 Skill Gap Roadmap")
    missing_list = top_role["Missing Skills"].split(", ")
    st.text(get_roadmap(missing_list))

    # =========================
    # CHART
    # =========================
    st.subheader("📈 Role Match Visualization")
    st.bar_chart(df.set_index("Role")["Match %"])

