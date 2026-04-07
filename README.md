# J.A.R.V.I.S - Enhanced AI Assistant

**J**ust **A**strong **R**ather **V**ery **I**ntelligent **S**ystem

A local-first AI assistant with a futuristic HUD, powered by Ollama. Features include voice control, document Q&A, web search, reminders, code execution, and system monitoring.

---

## 📦 What You Need Before Starting

| Requirement | How to Get It |
|-------------|---------------|
| **Windows 10/11** | You already have this |
| **Python 3.10 or higher** | Download from [python.org](https://python.org) |
| **Ollama** | Download from [ollama.com](https://ollama.com) |
| **Internet connection** | Only for first-time setup |

---

## 🚀 Complete Installation Guide (10 Minutes)

### Step 1: Install Python
1. Go to https://python.org/downloads
2. Click the yellow "Download Python" button
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" at the bottom
5. Click "Install Now"

### Step 2: Install Ollama
1. Go to https://ollama.com/download
2. Click "Download for Windows"
3. Run the installer
4. After installation, Ollama will start in system tray

### Step 3: Download JARVIS
**Option A (Easy):** Click the green "Code" button → "Download ZIP" → Extract folder

**Option B (Git users):** 
`git clone https://github.com/deandexter03-cmd/Jarvis.git`

### Step 4: Run the Setup (One Click!)
1. Open the JARVIS folder
2. **Double-click `setup.bat`** (I'll provide this file)
3. Wait for everything to install automatically
4. When done, **double-click `run.bat`**

### Step 5: Pull the AI Model
Open a Command Prompt and type:
ollama pull qwen3:1.7b
This downloads the AI brain (about 1GB). Takes 2-3 minutes.

### Step 6: Start JARVIS
1. Open a Command Prompt in the JARVIS folder
2. Type: `python jarvis.py`
3. OR just double-click `run.bat`

The HUD will open automatically!

---

## 🎮 How to Use JARVIS

### Voice Commands (Easiest Way)
1. In the HUD, click the **BLUE microphone button** 🎙️
2. Click "Allow" when browser asks for microphone access
3. Speak clearly! Examples:

| You Say | JARVIS Does |
|---------|-------------|
| "open chrome" | Opens Google Chrome |
| "battery status" | Tells you battery percentage |
| "take screenshot" | Captures and saves screenshot |
| "system status" | Shows CPU and RAM usage |
| "search for cute cats" | Searches the web |
| "tell me a joke" | Tells a programming joke |
| "remember that I like pizza" | Saves to memory |
| "what do you remember" | Recalls saved facts |
| "open youtube" | Opens YouTube in browser |
| "help" | Shows all commands |

### Typing Commands
Type commands in the input box and press "ENGAGE"

---

## 📁 What Each File Does

| File | Purpose |
|------|---------|
| `jarvis.py` | The main program (don't edit unless you know Python) |
| `jarvis_hud.html` | The visual interface (opens in your browser) |
| `setup.bat` | Installs everything automatically (run once) |
| `run.bat` | Starts JARVIS (run after setup) |
| `requirements.txt` | List of Python packages needed |
| `LICENSE` | Legal stuff (MIT = you can share freely) |

---

## 🔧 Troubleshooting

### "Python is not recognized"
- Python didn't install correctly
- Reinstall Python and CHECK "Add to PATH"

### "Ollama not responding"
- Make sure Ollama is running (check system tray)
- Or open Command Prompt and type: `ollama serve`

### "Port 5050 already in use"
- Close other programs using port 5050
- Or change line 85 in jarvis.py from 5050 to 5051

### Microphone not working
- Click "Allow" when browser asks for mic
- Check Windows mic settings
- Try Chrome or Edge browser (not Firefox)

### "Module not found" errors
- Run `setup.bat` again
- Or manually: `pip install -r requirements.txt`

### AI responses are slow
- Normal for first-time use on CPU
- Responses take 3-10 seconds
- For faster responses, use a smaller model: `ollama pull tinyllama`

---

## 💡 Pro Tips

1. **First run is slow** - The AI model loads into memory. Second run is faster.

2. **Keep Ollama running** - It needs to stay open in the background

3. **Use the blue mic button** - Browser mic is more accurate than Python's

4. **Index your documents** - Type `index myfile.txt` to let JARVIS read your files

5. **Set reminders** - Try `remind me to take break at 3pm`

---

## 📞 Getting Help

If something doesn't work:
1. Check the Troubleshooting section above
2. Open an Issue on GitHub
3. Make sure you have Python 3.10+ and Ollama installed

---

## 📜 License

MIT License - Free to use, share, and modify

---

## 🙏 Credits

- **OpenJarvis (Stanford University)** - Advanced features inspiration
- **Ollama** - Local AI inference engine
- **Edge TTS** - Voice synthesis

---

**Made with ⚡ by Dean Dexter**

*"Sometimes you have to run before you can walk." - Tony Stark*
