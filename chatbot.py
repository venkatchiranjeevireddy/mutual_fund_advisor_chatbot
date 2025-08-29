from dotenv import load_dotenv
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from groq import Groq
import traceback

load_dotenv(override=True)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def init_clients():
    groq_client = None
    gemini_client = None
    try:
        groq_client = Groq(api_key=os.getenv("GROP_API_KEY"))
    except Exception as e:
        print("Error initializing Groq:", e)
    try:
        # Try import Gemini client, skip if not available
        from gemini import Gemini
        gemini_client = Gemini(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception as e:
        print("Error initializing Gemini:", e)
    return groq_client, gemini_client

groq_client, gemini_client = init_clients()

def serper_search(query):
    if not SERPER_API_KEY:
        return "Serper API key not set."
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            snippet = data.get("organic", [{}])[0].get("snippet", "")
            return snippet or "No relevant info found."
        else:
            return f"Search API error: {response.status_code}"
    except Exception as e:
        return f"Search API exception: {str(e)}"

class Me:
    def __init__(self):
        self.name = "mutual funds Advisor"
        self.history = []  # list of [user_msg, bot_msg]

        self.linkedin = ""
        try:
            reader = PdfReader("ert.pdf")
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.linkedin += text
        except Exception as e:
            print("Error reading PDF:", e)
            self.linkedin = ""

    def system_prompt(self):
        prompt = (
            f"You are {self.name}, a financial advisor assistant specializing in mutual funds.\n\n"
            f"Instructions:\n"
            f"- For the first message, say: \"Hello! Welcome to our financial advisory services. How can we assist you today?\"\n"
            f"- ONLY answer questions strictly related to:\n"
            f"  * Mutual funds\n"
            f"  * Investment planning\n"
            f"  * Financial advisory services\n"
            f"  * SIP, portfolio management\n"
            f"  * Financial goals and planning\n"
            f"- Use the PDF document content for information whenever possible.\n"
            f"- If the user asks about current or live data such as 'current SIP value', 'today's market price', 'currency rates', or any time-sensitive info, mention that you may look it up using a search API.\n"
            f"- Answer financial questions briefly and concisely, without unnecessary details.\n"
            f"- If you cannot find the answer in the PDF or via search, politely respond: \"I don't know about that. I specialize in mutual funds and investment advisory. How can I help with your investments today?\"\n"
            f"- End financial advice replies with: \"For more info, contact us at 89***** or bvchiranjeevi54@gmail.com\"\n\n"
            f"PDF Content: {self.linkedin[:2000]}..."
        )
        return prompt

    def chat(self, message, history):
        if history is None:
            history = []

        # Build messages for LLM call
        messages = [{"role": "system", "content": self.system_prompt()}]
        
        # Add previous conversation history
        for msg in history:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            else:
                messages.append({"role": "assistant", "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": message})

        try:
            if groq_client:
                response = groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=messages,
                )
                content = response.choices[0].message.content.strip()
            else:
                raise Exception("Groq client not initialized")
        except Exception as e:
            print("Groq error:", e)
            print(traceback.format_exc())
            # Try Gemini fallback if available
            try:
                if gemini_client:
                    response = gemini_client.chat.completions.create(
                        model="gemini-1",
                        messages=messages,
                    )
                    content = response.choices[0].message.content.strip()
                else:
                    raise Exception("Gemini client not initialized")
            except Exception as e2:
                print("Gemini error:", e2)
                print(traceback.format_exc())
                content = (
                    "Sorry, I'm having trouble processing your request right now. "
                    "Please try again later or contact us directly."
                )

        # If answer seems like a generic failure or empty, try Serper fallback
        if not content or content.lower().startswith("sorry") or content.strip() == "":
            search_result = serper_search(message)
            if search_result and search_result != "No relevant info found.":
                content = f"I looked up your question and found this:\n\n{search_result}"
            else:
                content = "I don't know about that. I specialize in mutual funds and investment advisory. How can I help with your investments today?"

        return content

me = Me()

iface = gr.ChatInterface(
    fn=me.chat,
    type="messages"  # Use message dict format to avoid deprecation warnings
)

iface.launch()
