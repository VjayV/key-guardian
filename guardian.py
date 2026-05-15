import keyboard
import time
import pyperclip
from transformers import pipeline

# Initialize TinyBERT
print("-" * 30)
print("LOADING AI...")
guard_ai = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")
print("AI LOADED. State-Sync Version Active.")
print("INSTRUCTIONS:")
print(" - Type into any text field.")
print(" - Press SHIFT + ENTER to scan and send.")
print("-" * 30)

def scan_and_send():
    # --- STATE SYNC FIX ---
    # Instead of relying on a character buffer, grab the current text directly
    old_clipboard = pyperclip.paste()
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.1)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.1)
    current_content = pyperclip.paste()
    pyperclip.copy(old_clipboard)

    if not current_content.strip():
        return

    print(f"\nScanning Actual Content: '{current_content}'")
    
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

keyboard.add_hotkey('shift+enter', scan_and_send)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\nGuardian stopped.")
