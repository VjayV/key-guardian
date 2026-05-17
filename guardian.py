import keyboard
import time
import pyperclip
import pygetwindow as gw
import threading
from transformers import pipeline

#Initialize TinyBERT
print("-" * 30)
print("LOADING AI...")
guard_ai = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")
print("AI LOADED")

# --- CONFIGURATION ---
TARGET_APPS = ["Discord", "Notepad", "WhatsApp", "Outlook"] 
print(f"GUARDIAN ACTIVE ON: {', '.join(TARGET_APPS)}")
print("-" * 30)

def is_target_window_active():
    try:
        active_window = gw.getActiveWindow()
        if active_window is None: return False
        window_title = active_window.title.lower()
        return any(app.lower() in window_title for app in TARGET_APPS)
    except Exception:
        return False

def ai_analysis_task(content):
    print(f"\n[Async] Scanning: '{content}'")
    
    start = time.time()
    result = guard_ai(content)[0]
    duration = time.time() - start
    
    score = result['score']
    label = result['label']

    print(f"Result: {label} ({score:.2%}) | Time: {duration:.2f}s")

    if label == 'NSFW' and score > 0.8:
        print("❌ DANGER DETECTED. Message blocked.")
        print("Action: Manual intervention required to send.")
    else:
        print("✅ SAFE. Releasing message...")
        keyboard.press_and_release('right')
        keyboard.press_and_release('enter')

def handle_shift_enter():
    """Main logic triggered by hotkey."""
    if not is_target_window_active():
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
        keyboard.press_and_release('enter')
        return

    scanner_thread = threading.Thread(target=ai_analysis_task, args=(current_content,))
    scanner_thread.start()

keyboard.add_hotkey('shift+enter', handle_shift_enter, suppress=True)

try:
    print("Guardian is standing by. Press Shift+Enter to send safely.")
    keyboard.wait()
except KeyboardInterrupt:
    print("\nGuardian stopped.")
