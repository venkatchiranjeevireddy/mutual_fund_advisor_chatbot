# mutual_fund_advisor_chatbot
This project is an **AI-powered financial advisory assistant** specializing in **mutual funds, SIPs, and investment planning**.  
It uses **Groq LLM** as the primary model, with **Gemini** as a fallback, and integrates **Gradio** for a simple chat interface.  
Additionally, the bot can extract knowledge from a **PDF document (ert.pdf)** and perform **live searches** using the Serper API.  

---

## 🚀 Features
- AI chatbot specialized in **mutual funds and financial advisory**.  
- Uses **Groq (Llama3-8b-8192)** as the main LLM, with **Gemini** as a fallback model.  
- **PDF document ingestion** (ert.pdf) to enrich responses with relevant content.  
- **Serper API integration** for real-time information retrieval.  
- Built-in **conversation history** to maintain context.  
- Deployable as a **Gradio web app** with a clean chat interface.  
- Provides **contact details** for further advisory.  

---

## 🛠️ Tech Stack
- **Python 3.10+**  
- **Groq API** (LLM integration)  
- **Gemini API** (fallback LLM)  
- **Gradio** (chat interface)  
- **Serper API** (search)  
- **pypdf** (PDF parsing)  
- **dotenv** (environment variables)  
- **requests** (API calls)  

---

## 📂 Project Structure
```
project/
│── main.py          # Main chatbot code
│── ert.pdf          # Financial advisory knowledge source
│── requirements.txt # Python dependencies
│── .env             # API keys (Groq, Gemini, Serper)
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/venkatchiranjeevireddy/Engineering_team.git
cd Engineering_team
```

2. **Create & activate virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add API keys**  
Create a `.env` file in the project root:
```
GROP_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

5. **Run the chatbot**
```bash
python main.py
```

6. **Open in browser**  
The Gradio interface will launch at:
```
http://127.0.0.1:7860
```

---

## 📦 requirements.txt
```
gradio==3.41.0
python-dotenv==1.0.0
pypdf==3.17.4
requests==2.31.0
groq==0.5.0
```

*(Optional if you enable Gemini)*  
```
gemini
```

---

## 📌 Example Use Case
- User: *"Can you suggest a SIP plan for long-term investment?"*  
- Bot: *"Systematically investing in equity mutual funds through SIPs can help you achieve long-term wealth creation. For more info, contact us at 89***** or bvchiranjeevi54@gmail.com"*  

---

## 👨‍💻 Author
Developed by **Venkat Chiranjeevi Reddy**  
📧 Email: bvchiranjeevi54@gmail.com  
📞 Phone: 89*****  
