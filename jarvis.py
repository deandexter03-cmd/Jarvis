# Jarvis ULTIMATE EDITION v4.1 - FIXED & OPTIMIZED
# pip install speechrecognition edge-tts pygame pyautogui pygetwindow psutil requests flask flask-cors

import speech_recognition as sr
import os
import webbrowser
import time
import threading
from datetime import datetime
import random
import asyncio
import edge_tts
import pygame
import tempfile
import pyautogui
import pygetwindow as gw
import requests
import re
import psutil
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# ───────────────────────────────────────────────
#          CONFIG
# ───────────────────────────────────────────────
OLLAMA_MODEL = "qwen3:1.7b-q4_K_M"
OLLAMA_URL = "http://localhost:11434/api/generate"  # Changed to /generate (faster)

# ───────────────────────────────────────────────
#          FLASK BRIDGE
# ───────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

message_queue = []
chat_history = []

@app.route('/send', methods=['POST'])
def receive_from_hud():
    data = request.json
    cmd = data.get('command', '').strip()
    if cmd:
        message_queue.append(cmd)
    return jsonify({'status': 'ok'})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({'history': chat_history[-50:]})

@app.route('/status', methods=['GET'])
def get_status():
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        bat = psutil.sensors_battery()
        bat_pct = round(bat.percent) if bat else None
        bat_plugged = bat.power_plugged if bat else None
        disk = round(psutil.disk_usage('/').percent)
    except:
        cpu = ram = disk = 0
        bat_pct = None
        bat_plugged = False
    return jsonify({
        'cpu': round(cpu), 'ram': round(ram),
        'battery': bat_pct, 'plugged': bat_plugged,
        'disk': round(disk),
        'time': datetime.now().strftime('%H:%M:%S'),
        'date': datetime.now().strftime('%a %d %b %Y').upper()
    })

def push_chat(role, text):
    chat_history.append({
        'role': role,
        'text': text,
        'time': datetime.now().strftime('%H:%M')
    })

def run_flask():
    # FIXED: Removed the invalid 'quiet' parameter
    app.run(port=5050, debug=False, use_reloader=False)

# ───────────────────────────────────────────────
#          VOICE
# ───────────────────────────────────────────────
async def speak_jarvis(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp = f.name
        await edge_tts.Communicate(text, "en-GB-RyanNeural").save(tmp)
        pygame.mixer.init()
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.unlink(tmp)
    except:
        print(f"🔊 JARVIS: {text}")

def speak(text):
    try:
        asyncio.run(speak_jarvis(text))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speak_jarvis(text))
        loop.close()

# ───────────────────────────────────────────────
#          APP DATABASE (SIMPLIFIED)
# ───────────────────────────────────────────────
def find_app(cmd):
    apps = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
    }
    for name, exe in apps.items():
        if name in cmd.lower():
            return exe
    return None

# ───────────────────────────────────────────────
#          COMMANDS
# ───────────────────────────────────────────────
def take_screenshot():
    try:
        fn = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot().save(fn)
        os.startfile(fn)
        return "Screenshot captured, sir."
    except:
        return "Failed to capture screenshot, sir."

def get_battery():
    try:
        b = psutil.sensors_battery()
        if b:
            return f"Battery at {round(b.percent)}%, {'plugged in' if b.power_plugged else 'on battery'}, sir."
        return "No battery detected, sir."
    except:
        return "Unable to read battery, sir."

def get_system_status():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"CPU at {cpu}%, RAM at {ram}%, sir."
    except:
        return "Unable to read system status, sir."

# ───────────────────────────────────────────────
#          OLLAMA (FIXED PROMPT)
# ───────────────────────────────────────────────
def ask_ollama(question):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"You are JARVIS, an AI assistant. Be helpful and conversational. Answer naturally.\n\nUser: {question}\nJARVIS:",
                "stream": False,
                "options": {"num_predict": 256, "temperature": 0.7}  # Faster responses
            },
            timeout=30
        )
        if response.status_code == 200:
            reply = response.json().get("response", "").strip()
            if reply:
                return reply
        return fallback_response(question)
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
        return fallback_response(question)

def fallback_response(question):
    q = question.lower()
    if "hello" in q or "hi" in q:
        return "Hello sir, how can I help you today?"
    if "battery" in q:
        return get_battery()
    if "status" in q or "cpu" in q or "ram" in q:
        return get_system_status()
    if "time" in q:
        return f"It's {datetime.now().strftime('%I:%M %p')}, sir."
    if "joke" in q:
        return random.choice(["Why do programmers prefer dark mode? Because light attracts bugs!", "What do you call a fake noodle? An impasta!"])
    if "difference between cpu and ram" in q:
        return "The CPU processes instructions, sir, while RAM stores data temporarily for quick access. Think of CPU as the brain and RAM as the notepad."
    return f"I understand you're asking about '{question}', sir. I'm still learning, but I can help with system commands like 'battery status', 'system status', or 'open chrome'."

# ───────────────────────────────────────────────
#          LISTEN
# ───────────────────────────────────────────────
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...", end="\r")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio).lower().strip()
            print(f"\n✨ You: {text}")
            return text
        except:
            return ""

# ───────────────────────────────────────────────
#          PROCESS COMMAND
# ───────────────────────────────────────────────
def process_command(command):
    cmd = command.lower()
    
    # Quick commands (no AI needed)
    if "battery" in cmd:
        return get_battery()
    if "system status" in cmd or "cpu" in cmd or "ram" in cmd:
        return get_system_status()
    if "screenshot" in cmd:
        return take_screenshot()
    if "time" in cmd:
        return f"It's {datetime.now().strftime('%I:%M %p')}, sir."
    if "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube, sir."
    if "open google" in cmd:
        webbrowser.open("https://google.com")
        return "Opening Google, sir."
    if "open github" in cmd:
        webbrowser.open("https://github.com")
        return "Opening GitHub, sir."
    
    # Open apps
    if cmd.startswith(("open ", "launch ")):
        app_exe = find_app(cmd)
        if app_exe:
            os.system(f"start {app_exe}")
            return f"Opening {app_exe.replace('.exe','')}, sir."
        return f"Sorry sir, I don't know how to open that."
    
    # If no quick match, use AI
    return None

# ───────────────────────────────────────────────
#          HANDLE COMMAND
# ───────────────────────────────────────────────
def handle_command(command):
    push_chat('user', command)
    
    # Try quick commands first
    quick_response = process_command(command)
    if quick_response:
        print(f"🤖 JARVIS: {quick_response}")
        push_chat('jarvis', quick_response)
        speak(quick_response)
        return
    
    # Use AI for everything else
    print("🧠 Thinking...", end="\r")
    answer = ask_ollama(command)
    print(f"🤖 JARVIS: {answer}")
    push_chat('jarvis', answer)
    speak(answer)

# ───────────────────────────────────────────────
#          MAIN
# ───────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════╗")
    print("║    JARVIS - ULTIMATE EDITION v4.1       ║")
    print("║    🧠 Powered by Ollama (qwen3)         ║")
    print("║    🖥️  HUD Bridge on port 5050          ║")
    print("╚══════════════════════════════════════════╝")
    
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("✅ HUD bridge running on http://localhost:5050")
    
    # Open HUD
    hud_path = os.path.join(os.path.dirname(__file__), "jarvis_hud.html")
    if os.path.exists(hud_path):
        os.startfile(hud_path)
        print("🖥️  HUD opened!")
    else:
        print(f"⚠️  HUD not found at {hud_path}")
    
    # Test Ollama
    try:
        test = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": "Say online", "stream": False}, timeout=10)
        if test.status_code == 200:
            print("✅ Ollama connected - AI mode ready")
            speak("JARVIS online, sir. How may I assist?")
            push_chat('jarvis', 'JARVIS online. Ready for commands, sir.')
        else:
            raise Exception()
    except:
        print("⚠️  Ollama offline - using fallback mode")
        speak("JARVIS online in local mode, sir.")
        push_chat('jarvis', 'JARVIS online in local mode, sir.')
    
    print("\n🎯 Try saying or typing:")
    print("🔋 'battery status'     💻 'system status'")
    print("📸 'take screenshot'     🌐 'open youtube'")
    print("❓ 'what is Python?'      😄 'tell me a joke'")
    print("❌ 'exit' to stop\n")
    
    while True:
        # Check HUD commands
        if message_queue:
            cmd = message_queue.pop(0)
            print(f"\n🖥️  HUD: {cmd}")
            if cmd in ["exit", "quit", "bye", "goodnight"]:
                speak("Goodnight, sir.")
                break
            handle_command(cmd)
            time.sleep(0.3)
            continue
        
        # Voice commands
        command = listen()
        if command:
            if command in ["exit", "quit", "bye", "goodnight"]:
                speak("Goodnight, sir.")
                break
            handle_command(command)
            time.sleep(0.3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Until next time, sir.")