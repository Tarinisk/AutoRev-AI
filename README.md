# AutoRev-AI

AutoRev-AI is a web-based robot control system that lets a user operate a robot through a browser interface. The project combines a simple front-end dashboard with a Python backend that sends commands to a robot over UDP.

## What the project does

This application provides multiple control modes for a robot:

- Manual control using on-screen buttons or keyboard input
- Voice control with fuzzy command matching
- Autonomous mode selection from the main dashboard
- Live feed support for connecting to an IP webcam stream

The interface is designed as a lightweight web app so the robot can be controlled from a local machine or a browser-connected device.

## Main features

- Dashboard-style control page
- Manual movement controls with forward, backward, left, right, and stop actions
- Voice command parsing using fuzzy matching for natural language inputs
- Backend command relay to the robot over UDP
- Live feed integration for camera streaming

## Technologies and languages used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Communication and libraries
- Socket programming for UDP communication
- thefuzz for voice command matching and fuzzy logic

## Project structure

The main project files are located in the Project/AutoRev-AI folder:

- index.html – main mode selection page
- dashboard.html – main dashboard view
- manual.html – manual control interface
- voice.html – voice control interface
- autonomous.html – autonomous mode page
- robot_server.py – Flask server that receives commands and sends them to the robot
- script.js – shared JavaScript for command sending and navigation
- style.css – shared styling for the pages

## Setup and run

1. Install the required Python packages:

```bash
pip install flask thefuzz
```

2. Update the robot connection settings in robot_server.py:

- Change the ESP_IP value to the robot's IP address
- Adjust the PORT if needed

3. Start the backend server:

```bash
python robot_server.py
```

4. Open the web interface in your browser:

```bash
http://localhost:5000/
```

## Notes

- The web app is currently designed as a local or network-based control interface.
- The live feed feature depends on the availability of an IP webcam or compatible stream source.
- The robot connection details must be configured correctly for movement commands to reach the hardware.

## Future improvements

Possible enhancements include:

- Adding real autonomous navigation logic
- Improving voice command accuracy
- Adding a live camera stream viewer with better error handling
- Supporting more robot hardware and communication protocols
