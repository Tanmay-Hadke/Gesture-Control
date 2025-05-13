import cv2
import time
import numpy as np
import pyautogui
import speech_recognition as sr
import threading
import pyttsx3
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import handTrackingModule as htm

# ============ Setup ============
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon=0.7)
wScr, hScr = pyautogui.size()
frameR = 100
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
minVol, maxVol = volume.GetVolumeRange()[0:2]
volume_level = volume.GetMasterVolumeLevel()
volume_step = 1.5

# Mode control
mode_index = 0
mode_labels = ["Default", "Cursor", "Media"]
command_lock = threading.Lock()
playPauseFlag = False

# TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ============ Voice Command Thread ============
def listen_for_commands():
    global mode_index, exit_program
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized command: {command}")
                with command_lock:
                    if "default" in command:
                        mode_index = 0
                        speak("Default mode")
                    elif "cursor" in command:
                        mode_index = 1
                        speak("Cursor mode")
                    elif "media" in command:
                        mode_index = 2
                        speak("Media mode")
                    elif "stop" in command or "exit" in command:
                        exit_program = True
                        speak("Exiting program")
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")

# Start listening in background
exit_program = False
threading.Thread(target=listen_for_commands, daemon=True).start()

# ============ Main Loop ============
pTime = 0

while True:
    if exit_program:
        print("Exiting program...")
        cap.release()
        cv2.destroyAllWindows()
        break

    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # Check finger states (thumb, index, middle, ring, pinky)
        fingers.append(1 if lmList[4][1] > lmList[3][1] else 0)  # Thumb
        for tip in [8, 12, 16, 20]:
            fingers.append(1 if lmList[tip][2] < lmList[tip - 2][2] else 0)

        mode = mode_labels[mode_index]
        cv2.putText(img, f"Mode: {mode}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

        # ---------------- Cursor Mode ----------------
        if mode_index == 1:
            if fingers[1] == 1:
                x1, y1 = lmList[8][1], lmList[8][2]
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                if abs(clocX - plocX) > 1 or abs(clocY - plocY) > 1:
                    pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

                # Double click
                if fingers[1:3] == [1, 1]:
                    pyautogui.doubleClick()
                    time.sleep(0.3)

        # ---------------- Media Mode ----------------
        elif mode_index == 2:
            if len(fingers) == 5:
                # All fingers up – stop volume changes
                if all(f == 1 for f in fingers):
                    pass

                # Play/pause
                elif fingers[1] == 1 and fingers[2] == 1 and all(f == 0 for i, f in enumerate(fingers) if i not in [1, 2]):
                    if not playPauseFlag:
                        pyautogui.press("playpause")
                        print("Play/Pause toggled")
                        playPauseFlag = True
                else:
                    playPauseFlag = False

                # Thumb up only – increase volume
                if fingers[0] == 1 and all(f == 0 for i, f in enumerate(fingers) if i != 0):
                    volume_level = min(maxVol, volume_level + volume_step)
                    volume.SetMasterVolumeLevel(volume_level, None)
                    print(f"Volume Increased: {volume_level:.2f}")

                # Pinky up only – decrease volume
                elif fingers[4] == 1 and all(f == 0 for i, f in enumerate(fingers) if i != 4):
                    volume_level = max(minVol, volume_level - volume_step)
                    volume.SetMasterVolumeLevel(volume_level, None)
                    print(f"Volume Decreased: {volume_level:.2f}")

                # Display volume progress bar only when in Media mode
                progress_bar_length = 400  # Width of the progress bar
                filled_length = int((volume_level - minVol) / (maxVol - minVol) * progress_bar_length)
                cv2.rectangle(img, (50, hCam - 50), (50 + progress_bar_length, hCam - 30), (255, 255, 255), 3)  # Border
                cv2.rectangle(img, (50, hCam - 50), (50 + filled_length, hCam - 30), (0, 255, 0), cv2.FILLED)  # Filled part
                cv2.putText(img, f"Volume: {int((volume_level - minVol) / (maxVol - minVol) * 100)}%", (50, hCam - 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # ---------------- FPS ----------------
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime - pTime > 0 else 0
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (wCam - 150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Voice + Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
