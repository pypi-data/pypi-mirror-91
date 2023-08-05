import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ROUTING_KEY = os.getenv("route_key") # ENTER EVENTS V2 API INTEGRATION KEY HERE 

def trigger_incident():
    # Triggers a PagerDuty incident without a previously generated incident key
    # Uses Events V2 API - documentation: https://v2.developer.pagerduty.com/docs/send-an-event-events-api-v2

    header = {
        "Content-Type": "application/json"
    }

    payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": ROUTING_KEY, 
        "event_action": "trigger",
        "payload": {
            "summary": "BRS found!",
            "source": "monitoringtool:xxx",
            "severity": "critical"
        }
    }

    response = requests.post('https://events.pagerduty.com/v2/enqueue', 
                            data=json.dumps(payload),
                            headers=header)
    
    if response.json()["status"] == "success":
        print('Incident created with with dedup key (also known as incident / alert key) of ' + '"' + response.json()['dedup_key'] + '"') 
    else:
        print(response.text) # print error message if not successful
