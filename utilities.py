import requests
import canvas as c
import json
import os

def sortByAttr(data, attribute):
    # Use sorted with the attribute as the key
    descending = attribute.startswith("-")
    attribute = attribute[1:] if descending else attribute

    try:
        return attribute, sorted(
            data, 
            key=lambda item: normalizeValue(item[attribute]) if isinstance(item, dict) else float("inf"),
            reverse=descending
        )
    except KeyError:
        print(f"Invalid attribute: {attribute}")
        return attribute, sorted(
            data, 
            key=lambda item: normalizeValue(item["first"]) if isinstance(item, dict) else float("inf"),
            reverse=descending
        )
        # return data

def normalizeValue(value):
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

def getCanvasData(url, params={}, file=0):
    try:
        if file and os.path.exists("./cache/"+file+".json"):
            return readJSON(file)
        # print(f"API {c.canvasURL}{url}");

        response = requests.get(f"{c.canvasURL}{url}", headers=c.headers, params=params)
        if file:
            writeJSON(file, response.json())

        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"    - {e}")
        return {}
    
def writeJSON(fileName, data):
    # Write JSON data to file
    with open("./cache/"+fileName+".json", "w") as file:
        json.dump(data, file, indent=4)
        # print(f"Done writing {fileName}")


def readJSON(fileName):
    # Read JSON data from file and convert it back to a dictionary
    with open("./cache/"+fileName+".json", "r") as file:
        data = json.load(file)
        # print(f"Done reading {fileName}")
        return data
