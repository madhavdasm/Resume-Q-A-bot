import gradio as gr
import openai
import PyPDF2
import os
from io import BytesIO

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ["OPEN_API_KEY"]
)

# Global variable to store extracted resume text
current_resume_text = ""

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
       
        # Extract text from all pages
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
       
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def process_resume(pdf_file):
    """Process the uploaded resume and store text globally"""
    global current_resume_text
   
    if not pdf_file:
        return "Please upload a PDF file.", ""
   
    try:
        # Extract text from PDF
        current_resume_text = extract_text_from_pdf(pdf_file)
       
        if not current_resume_text:
            return "No text could be extracted from the PDF. Please ensure the PDF contains readable text.", ""
       
        success_message = f"✅ Resume processed successfully! ({len(current_resume_text)} characters extracted)\n\nYou can now ask questions about this resume in the chat below."
        return success_message, ""
       
    except Exception as e:
        current_resume_text = ""
        return f"Error processing resume: {str(e)}", ""

def answer_question(question, chat_history):
    """Answer questions about the uploaded resume"""
    global current_resume_text
   
    if not current_resume_text:
        response = "❌ Please upload and process a resume first before asking questions."
        chat_history.append([question, response])
        return chat_history, ""
   
    if not question.strip():
        response = "Please enter a question about the resume."
        chat_history.append([question, response])
        return chat_history, ""
   
    try:
        # Create prompt for OpenAI
        prompt = f"""
        Based on the following resume content, please answer the user's question accurately and concisely:
        Resume Content:
        {current_resume_text}
        User Question: {question}
        Please provide a clear, specific answer based only on the information available in the resume. If the information is not available in the resume, please state that clearly.
        """
       
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about resumes. Base your answers strictly on the resume content provided. Be concise but thorough."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
       
        answer = response.choices[0].message.content
        chat_history.append([question, answer])
        return chat_history, ""
       
    except openai.AuthenticationError:
        response = "❌ Authentication Error: Please check your OpenAI API key."
        chat_history.append([question, response])
        return chat_history, ""
    except openai.RateLimitError:
        response = "❌ Rate limit exceeded. Please try again later."
        chat_history.append([question, response])
        return chat_history, ""
    except openai.APIError as e:
        response = f"❌ OpenAI API Error: {str(e)}"
        chat_history.append([question, response])
        return chat_history, ""
    except Exception as e:
        response = f"❌ Error: {str(e)}"
        chat_history.append([question, response])
        return chat_history, ""

def clear_chat():
    """Clear the chat history"""
    return []

def get_sample_questions():
    """Return sample questions users can ask"""
    return [
        "What are the key technical skills mentioned?",
        "What is their educational background?",
        "What programming languages do they know?",
        "What are their notable achievements?",
        "What certifications do they have?",
        "Rate this resume on a scale of 1-10"
    ]

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple", secondary_hue="purple")) as demo:
    gr.Markdown(
        "<h1 style='text-align: center; color: #C084FC;'>AI Resume Q&A Assistant</h1>",
        elem_id="title"
    )
    gr.Markdown(
        "<p style='text-align: center; color: white;'>Upload a resume (PDF) and ask specific questions about the candidate's skills, experience, and qualifications.</p>"
    )
   
    with gr.Row():
        with gr.Column(scale=1):
            # Resume Upload Section
            gr.Markdown("### 📄 Upload Resume")
            pdf_input = gr.File(label="Upload PDF Resume", file_types=[".pdf"])
            process_button = gr.Button("Process Resume", variant="primary")
            status_text = gr.Textbox(label="Status", lines=3, interactive=False)
           
            # Sample Questions Section
            gr.Markdown("### 💡 Sample Questions")
            sample_questions = get_sample_questions()
            for i, question in enumerate(sample_questions):
                gr.Markdown(f"• {question}")
       
        with gr.Column(scale=2):
            # Q&A Chat Section
            gr.Markdown("### 💬 Ask Questions About the Resume")
            chatbot = gr.Chatbot(label="Q&A Chat", height=400)
           
            with gr.Row():
                question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about the resume...",
                    scale=4
                )
                ask_button = gr.Button("Ask", variant="primary", scale=1)
           
            with gr.Row():
                clear_button = gr.Button("Clear Chat", variant="secondary")
   
    # Event handlers
    process_button.click(
        fn=process_resume,
        inputs=[pdf_input],
        outputs=[status_text, question_input]
    )
   
    ask_button.click(
        fn=answer_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot, question_input]
    )
   
    question_input.submit(
        fn=answer_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot, question_input]
    )
   
    clear_button.click(
        fn=clear_chat,
        outputs=[chatbot]
    )

if __name__ == "__main__":
    print("Starting Resume Q&A Assistant...")
    demo.launch()
