import keyboard
import time
import pyperclip
import pygetwindow as gw  # New dependency: pip install pygetwindow
from transformers import pipeline

#Initialize TinyBERT
print("-" * 30)
print("LOADING AI...")
guard_ai = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")
print("AI LOADED. Window-Targeting Version Active.")

# --- CONFIGURATION ---
# Add the names of the apps you want to monitor (case-insensitive)
TARGET_APPS = ["Discord", "Notepad", "WhatsApp", "Outlook", "Teams"] 
print(f"GUARDIAN ACTIVE ON: {', '.join(TARGET_APPS)}")
print("-" * 30)

def is_target_window_active():
    """Checks if the currently focused window is in our target list."""
    try:
        active_window = gw.getActiveWindow()
        if active_window is None:
            return False
        
        window_title = active_window.title.lower()
        return any(app.lower() in window_title for app in TARGET_APPS)
    except Exception:
        return False

def scan_and_send():
    if not is_target_window_active():
        keyboard.release('shift')
        keyboard.press_and_release('enter')
        return
    old_clipboard = pyperclip.paste()
    
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.1) 
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.1) 
    
    current_content = pyperclip.paste()
    pyperclip.copy(old_clipboard)

    if not current_content.strip():
        return

    print(f"\nTarget App Detected. Scanning: '{current_content}'")
    
    result = guard_ai(current_content)[0]
    score = result['score']
    label = result['label']

    print(f"Result: {label} (Certainty: {score:.2%})")

    if label == 'NSFW' and score > 0.8:
        print("❌ DANGER DETECTED. Blocking send.")
    else:
        print("✅ SAFE. Sending...")
        keyboard.press_and_release('right') 
        keyboard.press_and_release('enter')

keyboard.add_hotkey('shift+enter', scan_and_send, suppress=True)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\nGuardian stopped.")
