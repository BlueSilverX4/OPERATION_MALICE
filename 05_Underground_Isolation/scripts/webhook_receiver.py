#!/usr/bin/env python3
from flask import Flask, request, jsonify
import datetime
import json

app = Flask(__name__)
ALERT_LOG = "/home/brandongregg/Operation_MALICE/05_Underground_Isolation/alerts/webhook_events.log"

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.json
    timestamp = datetime.datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "event": "MALLICE_ALERT_RECEIVED",
        "payload": data
    }
    
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    print(f"[*] Alert received at {timestamp}")
    return jsonify({"status": "success", "message": "Alert logged"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
