import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from verifier import verify_output


load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    st.error("API_KEY is missing. Please add it to your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


WORKFLOWS = {
    "cloud_sales": {
        "label": "Cloud sales lead qualifier",
        "example": (
            "Hi, we are a small company using old on premise servers. "
            "We want to move to Azure but are unsure about security and cost."
        ),
        "prompt": """
            You are a cloud sales lead qualification assistant.

            Read the customer or business enquiry and classify it for a cloud sales team.

            Return ONLY valid JSON.
            Do not include markdown.
            Do not include explanation.
            Do not include extra keys.

            The JSON must follow this exact structure:

            {
            "category": "cloud_migration",
            "pain_point": "short summary of the customer's main problem",
            "suggested_next_step": "practical next step for the sales or technical team"
            }

            The category must be exactly one of:
            - cloud_migration
            - cyber_security
            - microsoft_365
            - support
            - general
            """
        },
    "bug_report": {
        "label": "Bug report structurer",
        "example": (
            "The login page keeps failing after I reset my password. "
            "I get the reset email and change the password, but when I try to log in again, "
            "it says invalid credentials. This is stopping users from accessing their account."
        ),
        "prompt": """
            You are a software support assistant.

            Read the messy bug report and turn it into a structured bug report for an engineering team.

            Return ONLY valid JSON.
            Do not include markdown.
            Do not include explanation.
            Do not include extra keys.

            The JSON must follow this exact structure:

            {
            "title": "short bug title",
            "steps_to_reproduce": [
                "step one",
                "step two",
                "step three"
            ],
            "expected_result": "what the user expected to happen",
            "actual_result": "what actually happened",
            "likely_area": "authentication",
            "priority": "medium"
            }

            likely_area must be exactly one of:
            - authentication
            - frontend
            - backend
            - database
            - api
            - performance
            - unknown

            priority must be exactly one of:
            - low
            - medium
            - high
            """
        },
    "requirement": {
        "label": "Software requirement cleaner",
        "example": (
            "Our admin team keeps copying customer data from spreadsheets into the CRM. "
            "Sometimes they miss fields or create duplicates. We need a better way to upload, "
            "validate and check the data before it goes into the system."
        ),
        "prompt": """
        You are a business analyst and software requirements assistant.

        Read the messy stakeholder request and turn it into a clear software requirement.

        Return ONLY valid JSON.
        Do not include markdown.
        Do not include explanation.
        Do not include extra keys.

        The JSON must follow this exact structure:

        {
        "user_story": "As a type of user, I want a goal so that a benefit is achieved.",
        "acceptance_criteria": [
            "clear testable criterion one",
            "clear testable criterion two",
            "clear testable criterion three"
        ],
        "business_value": "why this requirement matters",
        "priority": "medium",
        "system_area": "part of the system affected"
        }

        priority must be exactly one of:
        - low
        - medium
        - high
        """
    }
}


def call_gemini(user_message: str, workflow: str) -> str:
    workflow_prompt = WORKFLOWS[workflow]["prompt"]

    prompt = f"""
    {workflow_prompt}

    User message:
    \"\"\"{user_message}\"\"\"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


st.set_page_config(page_title="AI Intake Assistant", layout="centered")

st.title("AI Intake Assistant")

st.write("Turn customer messages into structured JSON and validate the result.")

selected_workflow = st.selectbox(
    "Choose workflow",
    options=list(WORKFLOWS.keys()),
    format_func=lambda key: WORKFLOWS[key]["label"]
)

user_message = st.text_area(
    "Paste a message",
    value=WORKFLOWS[selected_workflow]["example"],
    height=180,
    key=f"message_{selected_workflow}"
)

if st.button("Generate and verify"):
    if not user_message.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Calling Gemini and checking the output..."):
            model_output = call_gemini(user_message, selected_workflow)
            result = verify_output(selected_workflow, model_output)

        st.subheader("Selected workflow")
        st.write(WORKFLOWS[selected_workflow]["label"])

        st.subheader("Input message")
        st.write(user_message)

        st.subheader("Model output")
        st.code(model_output, language="json")

        st.subheader("Cleaned output")
        st.code(result.get("cleaned_output", ""), language="json")

        st.subheader("Verifier result")

        if result["passed"]:
            st.success(f"Passed | Score: {result['score']}")
        else:
            st.error(f"Failed | Score: {result['score']}")

        st.write(result["reason"])