# Import necessary libraries
import streamlit as st
import docx2txt
import openai

# Your OpenAI API key (replace with your actual key)
openai.api_key = 'your-api-key'

def extract_text_from_docx(file):
    """Extract text from a DOCX file using docx2txt."""
    return docx2txt.process(file)

def ask_gpt3(question, document_text):
    """Use GPT-3 to answer a question based on the document content."""
    # Here you could add your rules or additional instructions for GPT-3.
    prompt = f"Document: {document_text}\n\nQuestion: {question}\nAnswer:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app interface
st.title('Word Document Interaction App')

# File uploader to accept Word documents
uploaded_file = st.file_uploader("Upload a Word document", type="docx")
if uploaded_file is not None:
    # Extract the document text
    document_text = extract_text_from_docx(uploaded_file)
    st.text_area("Document Content", value=document_text, height=300, disabled=True)
    
    # User input for asking questions
    question = st.text_input("Ask a question based on the document")
    
    if question:
        # Generate an answer using GPT-3
        answer = ask_gpt3(question, document_text)
        st.write(answer)
