import requests
import canvas as c

def sortByAttr(data, attribute, descending=False):
    # Use sorted with the attribute as the key
    try:
        return sorted(data, key=lambda item: normalize_value(item.get(attribute, "")), reverse=descending)
    except KeyError:
        print(f"Invalid attribute: {attribute}")
        return data
    

def normalize_value(value):
    """Convert values to a common type for comparison."""
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        try:
            # Attempt to convert to a number if possible
            num_value = float(value)
            return num_value if "." in value else int(num_value)
        except ValueError:
            # If not a number, return lowercase string for consistent sorting
            return value.lower()
    return value  # Return as-is for other types



def sendMessage(studentId, subject, body):
    payload = {
        "recipients": studentId,
        "subject": f"WDD 330 - {subject}",
        "body": f"{body}",
        "context_code": f"course_{c.courseId}",
        "bulk_message": True
    }
    response = requests.post(f"{c.canvasURL}/conversations?force_new=true", headers=c.headers, json=payload )
    return response.json()

def getCanvasData(url, params={}):
    try:
        response = requests.get(url, headers=c.headers, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"    - {e}")
        return {}