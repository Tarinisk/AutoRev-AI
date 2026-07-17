from flask import Flask, request, send_from_directory
import socket
from thefuzz import process
import os

ESP_IP = "10.109.205.241"   # <<< CHANGE THIS
PORT = 4210

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

app = Flask(__name__, static_folder='.')

# Enable CORS manually so the browser doesn't block requests from index.html
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

# Smart Command Mapping
COMMANDS = {
    "F": ["move forward", "go straight", "go ahead", "front", "advance", "move up"],
    "B": ["move backward", "go back", "reverse", "retreat", "move down"],
    "L": ["turn left", "go left", "rotate left", "spin left"],
    "R": ["turn right", "go right", "rotate right", "spin right"],
    "S": ["stop", "halt", "wait", "brake", "pause", "hold on"]
}

def get_best_command(text):
    # Flatten the list to search against all phrases
    all_phrases = {}
    for code, phrases in COMMANDS.items():
        for p in phrases:
            all_phrases[p] = code
            
    # Find the best match for the input text
    # process.extractOne returns (match, score)
    best_match, score = process.extractOne(text, list(all_phrases.keys()))
    
    print(f"Voice Input: '{text}' | Matched: '{best_match}' (Score: {score})")
    
    # If confidence is high enough (>60), return the code
    if score > 60:
        return all_phrases[best_match]
    return None

@app.route("/")
def home():
    return send_from_directory('.', 'dashboard.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('.', path)

@app.route("/cmd", methods=["POST", "OPTIONS"])
def send_cmd():
    if request.method == "OPTIONS":
        return {"status": "ok"} # Handle preflight request
        
    data = request.json
    raw_cmd = data.get("cmd", "")
    
    # Check if it's a direct code (single letter) or a voice phrase
    if len(raw_cmd) == 1 and raw_cmd in ["F", "B", "L", "R", "S", "V"]:
        final_cmd = raw_cmd
    elif raw_cmd.startswith("MODE") or raw_cmd.startswith("US") or raw_cmd.startswith("V"):
        final_cmd = raw_cmd
    else:
        # It's a voice sentence, use Fuzzy Logic
        final_cmd = get_best_command(raw_cmd.lower())
        
    if final_cmd:
        udp.sendto(final_cmd.encode(), (ESP_IP, PORT))
        return {"status": "OK", "sent": final_cmd, "original": raw_cmd}
    else:
        return {"status": "IGNORED", "reason": "Low confidence or unknown command"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
