# 🛡️ Key Guardian

Ever sent a message in Microsoft Teams or Outlook and immediately regretted it? **Key Guardian** maintains a real-time sync with your active text field. When you trigger a send, a local AI model (TinyBERT) performs a "pre-flight" scan of the entire message context to catch NSFW or unprofessional content before it’s too late.

- **If it's safe:** The message is sent instantly.
- **If it's risky:** The send command is blocked, giving you a chance to edit.

## ⚙️ Installation

1. **Clone the repository:**
   git clone https://github.com/VjayV/key-guardian.git
   cd key-guardian

2. **Install dependencies:**
   It is recommended to use a virtual environment (venv).
   pip install -r requirements.txt

4. **Run the script:**
   ⚠️ **IMPORTANT:** You must run your terminal as an **Administrator**. This is required for the keyboard library to hook into hardware events across different applications like Teams, Outlook, or Slack.
   python guardian.py

## ⌨️ How to Use
* **Type normally:** The script tracks your keys in the background.
* **Send Message:** Instead of just pressing Enter, use **SHIFT + ENTER**. 
* **The Gatekeeper:** The AI will analyze the buffer. If the NSFW score is below the threshold, it simulates an Enter keypress for you automatically.

## 🧠 The AI Model
This project uses the michellejieli/NSFW_text_classifier model via the HuggingFace Transformers library. It is a **TinyBERT** variant, chosen because it is:
* **Fast:** Optimized for CPU inference.
* **Local:** Your data never leaves your machine. Privacy is baked into the design.

## 🚧 Roadmap & Improvements
This project is currently a proof-of-concept. Future iterations will focus on:
* **Concurrency:** Moving AI inference to a separate thread to ensure the keystroke listener never "hangs."

## ⚖️ License
Distributed under the MIT License.

---
*Disclaimer: This tool is intended for personal productivity and professional safety. Ensure you comply with your organization's IT policies regarding background scripts.*
