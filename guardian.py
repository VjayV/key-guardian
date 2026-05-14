import keyboard
import time
from transformers import pipeline

# Initialize TinyBERT
print("-" * 30)
print("LOADING AI... (This takes about 30s the first time)")
guard_ai = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")
print("AI LOADED. Guardian is watching.")
print("INSTRUCTIONS:")
print(" - Type normally.")
print(" - Use SHIFT + ENTER to send a message safely.")
print(" - Watch this window for AI scores.")
print("-" * 30)

current_buffer = ""

def on_key(event):
    global current_buffer
    if event.event_type == keyboard.KEY_DOWN:
        if len(event.name) == 1: 
            current_buffer += event.name
        elif event.name == 'space':
            current_buffer += " "
        elif event.name == 'backspace':
            current_buffer = current_buffer[:-1]

def scan_and_send():
    global current_buffer
    if not current_buffer.strip():
        return

    print(f"\nScanning: '{current_buffer}'")
    
    start_time = time.time()
    result = guard_ai(current_buffer)[0]
    end_time = time.time()
    
    score = result['score']
    label = result['label']
    duration = end_time - start_time

    print(f"Scan took: {duration:.2f}s")
    print(f"Result: {label} (Certainty: {score:.2%})")

    if label == 'NSFW' and score > 0.8:
        print("❌ DANGER DETECTED. Blocking send.")
        print("Please re-read your last sentence for typos.")
    else:
        print("✅ SAFE. Sending...")
        keyboard.release('shift') # Prevent Shift+Enter becoming a new line
        keyboard.press_and_release('enter')
        current_buffer = "" # Clear buffer after successful send

# Hook the keyboard
keyboard.hook(on_key)
keyboard.add_hotkey('shift+enter', scan_and_send)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\nGuardian stopped by user.")
