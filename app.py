
import os
import time
import gradio as gr
from google import genai

# Gemini API
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

# Gemini response
def chatbot(message, history):

    if not message.strip():
        return "Please enter a message."

    prompt = """
You are Mini Gemini Student Assistant.

Help students with:
- Engineering subjects
- Programming
- Projects
- Viva preparation
- Simple technical explanations

Use simple English and clear step-by-step answers.
"""

    conversation = prompt + "\n\n"

    for item in history:
        if isinstance(item, dict):
            role = item.get("role", "")
            content = item.get("content", "")

            if role == "user":
                conversation += "User: " + str(content) + "\n"
            elif role == "assistant":
                conversation += "Assistant: " + str(content) + "\n"

    conversation += "User: " + message

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=conversation
            )

            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(4)
            else:
                return "Gemini is temporarily busy. Please try again."

# Web interface
demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 Mini Gemini Chatbot",
    description="Your AI Student Assistant powered by Gemini",
    textbox=gr.Textbox(
        placeholder="Ask me anything..."
    )
)

demo.launch()
