import json
import re


def clean_model_output(model_output):
    
    cleaned = model_output.strip()

    cleaned = re.sub(r"^```json", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^```", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace != -1 and last_brace != -1:
        cleaned = cleaned[first_brace:last_brace + 1]

    return cleaned


def parse_json(model_output):
    cleaned_output = clean_model_output(model_output)

    try:
        data = json.loads(cleaned_output)
        return data, cleaned_output, None
    except json.JSONDecodeError:
        return None, cleaned_output, "Response could not be parsed as valid JSON."


def check_required_fields(data: dict, required_fields):
    return [field for field in required_fields if field not in data]


def check_empty_fields(data, fields):
    empty_fields = []

    for field in fields:
        value = data.get(field)

        if isinstance(value, str) and not value.strip():
            empty_fields.append(field)

        if isinstance(value, list) and len(value) == 0:
            empty_fields.append(field)

    return empty_fields


def verify_cloud_sales_output(model_output):
    required_fields = ["category", "pain_point", "suggested_next_step"]

    allowed_categories = [
        "cloud_migration",
        "cyber_security",
        "microsoft_365",
        "support",
        "general"
    ]

    data, cleaned_output, error = parse_json(model_output)

    if error:
        return {
            "passed": False,
            "score": 0,
            "reason": error,
            "cleaned_output": cleaned_output
        }

    missing_fields = check_required_fields(data, required_fields)

    if missing_fields:
        return {
            "passed": False,
            "score": 40,
            "reason": f"Missing required fields: {', '.join(missing_fields)}",
            "cleaned_output": cleaned_output
        }

    if data["category"] not in allowed_categories:
        return {
            "passed": False,
            "score": 60,
            "reason": f"The category must be one of: {', '.join(allowed_categories)}.",
            "cleaned_output": cleaned_output
        }

    empty_fields = check_empty_fields(data, required_fields)

    if empty_fields:
        return {
            "passed": False,
            "score": 70,
            "reason": f"These fields are empty: {', '.join(empty_fields)}",
            "cleaned_output": cleaned_output
        }

    return {
        "passed": True,
        "score": 100,
        "reason": "Valid cloud sales output with required fields and allowed category.",
        "cleaned_output": cleaned_output
    }


def verify_bug_report_output(model_output):
    required_fields = [
        "title",
        "steps_to_reproduce",
        "expected_result",
        "actual_result",
        "likely_area",
        "priority"
    ]

    allowed_areas = [
        "authentication",
        "frontend",
        "backend",
        "database",
        "api",
        "performance",
        "unknown"
    ]

    allowed_priorities = ["low", "medium", "high"]

    data, cleaned_output, error = parse_json(model_output)

    if error:
        return {
            "passed": False,
            "score": 0,
            "reason": error,
            "cleaned_output": cleaned_output
        }

    missing_fields = check_required_fields(data, required_fields)

    if missing_fields:
        return {
            "passed": False,
            "score": 40,
            "reason": f"Missing required fields: {', '.join(missing_fields)}",
            "cleaned_output": cleaned_output
        }

    if not isinstance(data["steps_to_reproduce"], list):
        return {
            "passed": False,
            "score": 55,
            "reason": "steps_to_reproduce must be a list.",
            "cleaned_output": cleaned_output
        }

    if data["likely_area"] not in allowed_areas:
        return {
            "passed": False,
            "score": 60,
            "reason": f"likely_area must be one of: {', '.join(allowed_areas)}.",
            "cleaned_output": cleaned_output
        }

    if data["priority"] not in allowed_priorities:
        return {
            "passed": False,
            "score": 60,
            "reason": f"priority must be one of: {', '.join(allowed_priorities)}.",
            "cleaned_output": cleaned_output
        }

    empty_fields = check_empty_fields(data, required_fields)

    if empty_fields:
        return {
            "passed": False,
            "score": 70,
            "reason": f"These fields are empty: {', '.join(empty_fields)}",
            "cleaned_output": cleaned_output
        }

    return {
        "passed": True,
        "score": 100,
        "reason": "Valid bug report output with required fields, list format and allowed values.",
        "cleaned_output": cleaned_output
    }


def verify_requirement_output(model_output):
    required_fields = [
        "user_story",
        "acceptance_criteria",
        "business_value",
        "priority",
        "system_area"
    ]

    allowed_priorities = ["low", "medium", "high"]

    data, cleaned_output, error = parse_json(model_output)

    if error:
        return {
            "passed": False,
            "score": 0,
            "reason": error,
            "cleaned_output": cleaned_output
        }

    missing_fields = check_required_fields(data, required_fields)

    if missing_fields:
        return {
            "passed": False,
            "score": 40,
            "reason": f"Missing required fields: {', '.join(missing_fields)}",
            "cleaned_output": cleaned_output
        }

    if not isinstance(data["acceptance_criteria"], list):
        return {
            "passed": False,
            "score": 55,
            "reason": "acceptance_criteria must be a list.",
            "cleaned_output": cleaned_output
        }

    if data["priority"] not in allowed_priorities:
        return {
            "passed": False,
            "score": 60,
            "reason": f"priority must be one of: {', '.join(allowed_priorities)}.",
            "cleaned_output": cleaned_output
        }

    empty_fields = check_empty_fields(data, required_fields)

    if empty_fields:
        return {
            "passed": False,
            "score": 70,
            "reason": f"These fields are empty: {', '.join(empty_fields)}",
            "cleaned_output": cleaned_output
        }

    return {
        "passed": True,
        "score": 100,
        "reason": "Valid requirement output with user story, acceptance criteria and allowed priority.",
        "cleaned_output": cleaned_output
    }


def verify_output(workflow: str, model_output):
    if workflow == "cloud_sales":
        return verify_cloud_sales_output(model_output)

    if workflow == "bug_report":
        return verify_bug_report_output(model_output)

    if workflow == "requirement":
        return verify_requirement_output(model_output)

    return {
        "passed": False,
        "score": 0,
        "reason": "Unknown workflow selected.",
        "cleaned_output": model_output
    }