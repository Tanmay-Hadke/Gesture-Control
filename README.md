
# 🎮 Voice + Hand Gesture Control System

A real-time **voice-activated and gesture-controlled system** using OpenCV, MediaPipe, and PyAutoGUI for smart human-computer interaction. This Python-based project enables users to control the mouse cursor and media functions (like volume and playback) through hand gestures and switch modes using voice commands.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/OpenCV-4.x-green" />
  <img src="https://img.shields.io/badge/MediaPipe-Hands-orange" />
  <img src="https://img.shields.io/badge/PyAutoGUI-Automation-lightgrey" />
  <img src="https://img.shields.io/badge/SpeechRecognition-Voice Control-red" />
</p>

---

## 🧠 Project Summary

This system uses:
- **Computer vision** for real-time hand gesture recognition using `MediaPipe`
- **Voice recognition** for mode switching using `SpeechRecognition` and `pyttsx3`
- **PyAutoGUI** for controlling mouse and keyboard actions
- **PyCAW (Core Audio APIs)** for Windows audio control

### 🔁 Modes:
| Mode        | Trigger                     | Functionality                                                                 |
|-------------|-----------------------------|-------------------------------------------------------------------------------|
| **Default** | "default" (voice)           | Idle state, no active control                                                 |
| **Cursor**  | "cursor" (voice)            | Move mouse with index finger, double click with index + middle fingers        |
| **Media**   | "media" (voice)             | Control volume (thumb/pinky), play/pause (index+middle), visual volume bar    |

---

## 🖥️ Features

### ✋ Hand Gesture Controls
- **Cursor Mode**:
  - ☝️ Index Finger Up → Move mouse cursor
  - ✌️ Index + Middle Fingers → Double click

- **Media Mode**:
  - 👍 Thumb Up → Increase volume
  - 🤙 Pinky Up → Decrease volume
  - ✌️ Index + Middle → Toggle play/pause
  - 🖐 All Fingers → Stop volume change

### 🎤 Voice Commands
Control mode hands-free using:
- `"default"` – switch to idle
- `"cursor"` – activate cursor mode
- `"media"` – activate media control mode
- `"stop"` / `"exit"` – exit the program

### 🔊 Real-Time Feedback
- On-screen overlays for mode and FPS
- Live volume level bar in media mode

---

## 📦 Requirements

Install dependencies using `pip`:

```bash
pip install opencv-python mediapipe pyautogui pyttsx3 speechrecognition comtypes pyaudio pycaw numpy
```

> 🔧 On Windows, install `PyAudio` with:
> ```
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 📁 File Structure

```
.
├── gesture_control.py        # Main application file
├── handTrackingModule.py     # Module for hand detection and tracking using MediaPipe
├── README.md                 # Project documentation
```

---

## 🚀 How to Run

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Tanmay-Hadke/Gesture-Control.git
   cd Gesture-Control
   ```

2. **Run the program:**
   ```bash
   python gesture_control.py
   ```

3. **Allow microphone access** and speak one of the supported voice commands.

---

## 🛠️ Customize or Extend

You can extend the system with:
- **Gesture-based app launching**
- **Air drawing or annotation**
- **Two-hand gesture recognition**
- **Dynamic gesture training using ML models**

---

## 📸 Demo

> Add your GIFs or screen recording here

---

## 🤝 Contribution

Contributions are welcome!

1. Fork the repo
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m "Added new feature"`
4. Push and open a pull request

---

## 🧑‍💻 Author

**Tanmay Hadke**   
🌐 [Github](https://yourwebsite.com)

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [MediaPipe by Google](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [PyCAW](https://github.com/AndreMiras/pycaw)
