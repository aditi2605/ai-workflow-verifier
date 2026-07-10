## AI Workflow Verifier

A small Python and Streamlit app that uses an LLM to structure messy messages and validate the output against expected rules.

---

## Overview

AI Workflow Verifier is a small project built with Python, Streamlit and the Gemini API.

The app takes an unstructured message, sends it to an LLM, and asks for a structured JSON response. It then verifies whether the response is usable by checking the format, required fields, allowed values and empty fields.

The app currently supports three workflows:

- **Cloud sales lead qualifier**: structures customer enquiries by identifying the category, pain point and suggested next step.
- **Bug report structurer**: turns unclear user issues into structured bug reports for an engineering team.
- **Software requirement cleaner**: turns rough stakeholder requests into clearer user stories, acceptance criteria and business value.

This is not intended to be a large production system. I built it to practise working with LLM APIs, prompt design, JSON validation and simple verification logic around AI output.

---

## Why I built this

LLMs can be useful, but they do not always return responses in the exact format an application expects. They may return markdown, miss required fields, add extra text, or produce an output that does not match the workflow.

I wanted to build something that goes beyond a basic chatbot and shows how AI output can be checked before it is treated as usable.

The main idea is simple:

> Generate the output, then verify it.

---

## What the app does

The app allows a user to:

- choose a workflow
- paste a messy business, customer or software message
- send the message to Gemini
- receive a structured JSON response
- check whether the response passes validation
- see a pass or fail result, score and reason

---

## Workflows

### 1. Cloud sales lead qualifier

This workflow structures a customer enquiry for a cloud sales or technical team.

Example input:

```text
Hi, we are a small company using old on-premise servers. We want to move to Azure but are unsure about security and cost.
```

Expected structured output:

```json
{
  "category": "cloud_migration",
  "pain_point": "The company is using old on-premise servers and is unsure about Azure migration, security and cost.",
  "suggested_next_step": "Arrange a discovery call to understand their current infrastructure, security concerns and migration goals."
}
```

Allowed categories:

```text
cloud_migration
cyber_security
microsoft_365
support
general
```

Required fields:

```text
category
pain_point
suggested_next_step
```

---

### 2. Bug report structurer

This workflow takes an unclear user issue and turns it into a clearer bug report for an engineering team.

Example input:

```text
The login page keeps failing after I reset my password. I get the reset email and change the password, but when I try to log in again, it says invalid credentials. This is stopping users from accessing their account.
```

Expected structured output:

```json
{
  "title": "Login fails after password reset",
  "steps_to_reproduce": [
    "Request a password reset",
    "Change the password using the reset email",
    "Return to the login page",
    "Try logging in with the new password"
  ],
  "expected_result": "The user should be able to log in successfully with the new password.",
  "actual_result": "The system shows an invalid credentials error.",
  "likely_area": "authentication",
  "priority": "high"
}
```

Allowed likely areas:

```text
authentication
frontend
backend
database
api
performance
unknown
```

Allowed priorities:

```text
low
medium
high
```

Required fields:

```text
title
steps_to_reproduce
expected_result
actual_result
likely_area
priority
```

---

### 3. Software requirement cleaner

This workflow takes a rough stakeholder request and turns it into a clearer software requirement.

Example input:

```text
Our admin team keeps copying customer data from spreadsheets into the CRM. Sometimes they miss fields or create duplicates. We need a better way to upload, validate and check the data before it goes into the system.
```

Expected structured output:

```json
{
  "user_story": "As an admin user, I want to upload and validate customer data before it enters the CRM so that I can reduce missing fields and duplicate records.",
  "acceptance_criteria": [
    "The user can upload customer data from a spreadsheet.",
    "The system highlights missing required fields.",
    "The system detects possible duplicate records before import."
  ],
  "business_value": "Reduces manual data entry errors and improves CRM data quality.",
  "priority": "medium",
  "system_area": "CRM data import"
}
```

Allowed priorities:

```text
low
medium
high
```

Required fields:

```text
user_story
acceptance_criteria
business_value
priority
system_area
```

---

## Verification logic

Each workflow has its own verifier rules.

The verifier checks whether the LLM response is usable for the selected workflow. It checks things such as:

- whether the response can be parsed as valid JSON
- whether all required fields are present
- whether fields that should be lists are returned as lists
- whether values such as category, likely area and priority are within the allowed options
- whether important fields are not empty

If the output passes, the app returns a score of `100`.

If the output fails, the app shows a lower score and explains what went wrong.

Example verifier result:

```json
{
  "passed": true,
  "score": 100,
  "reason": "Valid response with required fields and allowed values."
}
```

---

## Tech stack

```text
Python
Streamlit
Gemini API
python-dotenv
JSON validation
```

---



## How to run locally

Clone the repository:

```bash
git clone https://github.com/aditi2605/ai-workflow-verifier.git
cd ai-workflow-verifier
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

---

## What I learnt

While building this project, I practised:

- calling an LLM API from a Python application
- writing prompts for structured JSON output
- handling cases where the model returns markdown or invalid JSON
- validating model output against expected rules
- creating separate validation rules for different workflows
- building a simple Streamlit interface
- keeping API keys out of source control

The main learning point was that AI output should not be trusted automatically. Even when a prompt asks for a specific format, the application still needs checks around the result.

---

## Next steps

Planned improvements include:

- improving validation feedback when an output fails
- showing suggested fixes for failed responses
- adding clearer examples for each workflow
- improving the interface layout
- adding basic tests for the verifier functions

---

## Status

The app currently supports three workflows:

- cloud sales lead qualification
- bug report structuring
- software requirement cleaning

Each workflow has its own prompt structure and verifier rules. The next step is to improve the validation feedback and make the interface easier to use.