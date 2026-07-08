import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from verifier import verify_cloud_sales_output

load_dotenv()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

def call_gemini(user_message):
    prompt = f""" 
    You are a cloud sales lead qualification assistant.

    Your task is to read a customer or business enquiry and classify it for a cloud sales team.

    Return ONLY valid JSON.
    Do not include markdown.
    Do not include explanation.
    Do not create a coding problem.
    Do not include extra keys.

    The JSON must follow this exact structure:

    {{
    "category": "cloud_migration",
    "pain_point": "short summary of the customer's main problem",
    "suggested_next_step": "practical next step for the sales or technical team"
    }}

    The category must be exactly one of:
    - cloud_migration
    - cyber_security
    - microsoft_365
    - support
    - general

    Customer message:
    \"\"\"{user_message}\"\"\"
    """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()

st.set_page_config(page_title="AI Workflow Verifier", layout="centered")

st.title("AI Workflow Verifier")
st.write(
    "This app uses an LLM to turn messy business messages into structured output, "
    "then verifies whether the response follows expected rules."
)

example_message = (
    "Hi, we are a small company using old on premise servers. "
    "We want to move to Azure but are unsure about security and cost."
)

user_message = st.text_area(
    "Paste a customer or business message",
    value=example_message,
    height=160
)

if st.button("Run verifier"):
    if not user_message.strip():
        st.warning("Please enter a mssage first.")
    else:
        with st.spinner("Calloing Gemini and chacking the output..."):
            model_output = call_gemini(user_message)
            result = verify_cloud_sales_output(model_output)
        
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
          