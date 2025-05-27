

# 🧠 AI Resume Q\&A Assistant

Ask intelligent questions about any resume with the help of OpenAI's language models. This app extracts text from a PDF resume and allows users to query it using natural language. Built using **Gradio** and **OpenAI GPT-3.5 Turbo**.

[![Hugging Face Spaces](https://img.shields.io/badge/🧠_Try_on-HuggingFace-ffcc00?style=for-the-badge)](https://huggingface.co/spaces/madhavdasm/Resumebot)

---

## 🚀 Features

* 🔍 Upload any **PDF Resume**
* 🤖 Ask **natural language questions** like:

  * "What are their technical skills?"
  * "Where did they study?"
  * "What languages do they know?"
* 🧠 Powered by **OpenAI GPT-3.5 Turbo**
* 🎨 Simple & clean **Gradio UI**

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-qa-assistant.git
cd resume-qa-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure the following packages are included in `requirements.txt`:

```
openai
gradio
PyPDF2
```

### 3. Set OpenAI API Key

Set your OpenAI API key as an environment variable:

**Linux/Mac**

```bash
export OPEN_API_KEY=your_openai_key_here
```

**Windows (Command Prompt)**

```cmd
set OPEN_API_KEY=your_openai_key_here
```

---

## 🧪 Run the App

```bash
python hdfc_faq_chatbot.py
```

The app will launch locally in your browser.

---

## 🧠 Sample Questions to Try

* What are the key technical skills mentioned?
* What is their educational background?
* What programming languages do they know?
* What certifications do they have?
* Rate this resume on a scale of 1-10

---

## 📍 Live Demo

🟢 Try it live on **Hugging Face Spaces**:
👉 [https://huggingface.co/spaces/madhavdasm/Resumebot](https://huggingface.co/spaces/madhavdasm/Resumebot)

---

## 📌 Folder Structure

```
.
├── hdfc_faq_chatbot.py       # Main app file
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

Pull requests and suggestions are welcome!
If you find a bug or want a new feature, feel free to [open an issue](https://github.com/yourusername/resume-qa-assistant/issues).

---



