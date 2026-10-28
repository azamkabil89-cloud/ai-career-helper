
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Career Copilot")
st.write("Your personal AI career assistant.")

tool = st.selectbox(
    "Choose your tool",
    [
        "ATS Resume Analyzer",
        "AI Learning Roadmap",
        "AI Interview Coach"
    ]
)

if tool == "ATS Resume Analyzer":
    st.subheader("Resume Analyzer")
    role = st.text_input("Target job title")
    resume = st.text_area("Paste your resume")
    job = st.text_area("Paste the job description")

elif tool == "AI Learning Roadmap":
    st.subheader("Learning Roadmap")
    role = st.text_input("Career you want to learn")
    resume = st.text_area("Your current skills and experience")
    job = ""

else:
    st.subheader("Interview Coach")
    role = st.text_input("Target job title")
    resume = st.text_area("Your practice interview answer")
    job = ""

if st.button("Generate AI Results", type="primary"):
    if not role.strip() or not resume.strip():
        st.warning("Please complete the required fields.")
    elif tool == "ATS Resume Analyzer" and not job.strip():
        st.warning("Please add the job description.")
    else:
        try:
            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"]
            )

            prompts = {
                "ATS Resume Analyzer": (
                    "Review the resume against the job description. "
                    "Give an estimated compatibility score out of 100, "
                    "matching skills, missing keywords, and improvements. "
                    "Explain that the score is an estimate, not a real ATS score. "
                    "Never invent qualifications."
                ),
                "AI Learning Roadmap": (
                    "Create a beginner-friendly 12-week learning roadmap "
                    "for the target career. Include weekly goals, free "
                    "resources, practical projects, and portfolio advice. "
                    "Identify any assumptions clearly."
                ),
                "AI Interview Coach": (
                    "Review this interview answer for relevance, clarity, "
                    "structure, and examples. Suggest improvements and "
                    "provide a sample improved answer without inventing "
                    "the candidate's personal experience."
                )
            }

            details = f"Target role: {role}\n"

            if tool == "ATS Resume Analyzer":
                details += (
                    f"\nResume:\n{resume}\n"
                    f"\nJob description:\n{job}"
                )
            elif tool == "AI Learning Roadmap":
                details += f"\nCurrent skills:\n{resume}"
            else:
                details += f"\nInterview answer:\n{resume}"

            with st.spinner("AI is working..."):
                client = OpenAI(
                    api_key=st.secrets["OPENAI_API_KEY"]
                )
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=prompts[tool],
                    input=details
                )

            st.subheader("Your Results")
            st.markdown(response.output_text)

        except Exception as error:
            st.error(
                "Unable to generate results. Check your API key, "
                "API access, and available credits."
            )
            st.caption(str(error))
