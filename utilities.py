import requests
import canvas as c

def sortByAttr(data, attribute):
    try:
        # Use sorted with the attribute as the key
        return sorted(data, key=lambda item: item[attribute])
    except KeyError:
        print(f"Invalid attribute: {attribute}")
        return data

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
    response = requests.get(url, headers=c.headers, params=params)
    return response.json()