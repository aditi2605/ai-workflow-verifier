# AI Workflow Verifier

AI Workflow Verifier is a small Python and Streamlit project that uses an LLM to turn a messy customer message into structured JSON, then checks whether the response follows a set of expected rules.

The first workflow focuses on cloud sales lead qualification. A user can paste a customer enquiry, and the app asks Gemini to extract the main category, pain point and suggested next step. The verifier then checks whether the response is valid JSON, includes the required fields and uses an allowed category.

This project is not intended to be a large production system. I built it to practise working with LLM APIs, prompt design, JSON validation and simple verification logic around AI output.

## Why I built this

LLMs can be useful, but they do not always return responses in the format an application expects. They may return markdown, miss required fields, add extra text or produce an output that is not useful for the workflow.

I wanted to build a small project that shows how an AI response can be checked before it is treated as usable. The aim was to go beyond a basic chatbot and think more about how AI output could fit into a real software or business process.

## What the app does

The current version allows a user to:

- paste a customer or business message
- send the message to Gemini
- receive a structured JSON response
- check whether the response passes validation
- see a score and reason for the result

Example input:

```text
Hi, we are a small company using old on premise servers. We want to move to Azure but are unsure about security and cost.

Expected structured output:

{
  "category": "cloud_migration",
  "pain_point": "The company is using old on premise servers and is unsure about Azure migration, security and cost.",
  "suggested_next_step": "Arrange a discovery call to understand their current infrastructure, security concerns and migration goals."
}

## The verifier checks:

- Whether the response is valid JSON
- Whether all required fields are present
- Whether the category is one of the allowed values
- Whether important fields are not empty
- Current workflow
- Cloud sales lead qualifier

This workflow is designed to structure a customer enquiry for a cloud sales or technical team.

## Allowed categories:

cloud_migration
cyber_security
microsoft_365
support
general

## Required fields:

## category
pain_point
suggested_next_step

## Tech stack
Python
Streamlit
Gemini API
JSON validation


# How to run locally

-Clone the repository:
-git clone https://github.com/aditi2605/ai-workflow-verifier.git
-cd ai-workflow-verifier
-Create and activate a virtual environment:
-python3 -m venv .venv
-source .venv/bin/activate

##Install dependencies:
-pip install -r requirements.txt
-Create a .env file in the project root:
-GEMINI_API_KEY=your_api_key_here

##Run the app:
-streamlit run app.py

# What I learnt

While building this project, I practised:
-calling an LLM API from a Python application
-writing prompts for structured JSON output
-handling cases where the model returns markdown or invalid JSON
-validating model output against expected rules
-using Streamlit to build a simple interface
-keeping API keys out of source control

## The main learning point was that AI output should not be trusted automatically. Even when the prompt asks for a specific format, the application still needs checks around the result.

##Planned improvements:
I would like to extend the app with more workflows, such as:
-bug report structuring
-software requirement cleaning
-scoring model outputs with more detailed validation rules
-showing suggested fixes when an output fails validation

These improvements would make the project more useful across software engineering, support and business workflows.

##Status
This is an early version of the project. The first workflow is working locally, and the next step is to add more workflow types and improve the validation logic.