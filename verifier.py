import json
import re

Required_Fields = ["category", "pain_point", "suggested_next_step"]

allowed_categories = [
        "cloud_migration",
        "cyber_security",
        "microsoft_365",
        "support",
        "general"
    ]

def clean_model_output(model_output):
    """
    "Removes markdown code fences if the model returns JSON like:"
    ```json
    {...}
    ```
    """
    cleaned = model_output.strip()

    cleaned = re.sub(r"^```json", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^```", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    return cleaned

def verify_cloud_sales_output(model_output):
    cleaned_output = clean_model_output(model_output)
    try:
        data = json.loads(model_output)
    except json.JSONDecodeError:
        return {
            "passed": False,
            "score": 0,
            "reason": "The response is not valid JSON.",
            "clean_output": clean_output
        }
    
    missing_fields = [field for field in Required_Fields if field not in data]

    if missing_fields:
        return {
            "passed": False,
            "score": 40,
            "reason": f"Missing required fields: {', '.join(missing_fields)}"
        }
    


    if data["category"] not in allowed_categories:
        return {
            "passed": False,
            "score": 60,
            "reason": "The category is not one of the allowed values.",
            "cleaned_output": cleaned_output
        }
    if not str(data["pain_point"]).strip():
        return {
            "passed": False,
            "score": 70,
            "reason": "Valid response with required fields and allowed category.",
            "cleaned_output": cleaned_output
        }
    
    if not str(data["suggested_next_step"]).strip():
        return {
            "passed": False,
            "score": 70,
            "reason": "The suggested_next_step field is empty.",
            "cleaned_output": cleaned_output
        }

    return {
        "passed": True,
        "score": 100,
        "reason": "Valid response with required fields and allowed category.",
        "cleaned_output": cleaned_output
    }