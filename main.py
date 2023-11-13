# Install the necessary packages before running this script:
# pip install streamlit python-docx openai

import streamlit as st
from docx import Document
import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'your-api-key'

def read_docx(file):
    """Read the content of a docx file and return it as plain text."""
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def ask_gpt3(question, document_content, rules):
    """Use GPT-3 to answer a question based on the document content and rules."""
    prompt = f"{rules}\n\n{document_content}\n\nQuestion: {question}\nAnswer:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

st.title('Word Document QA with Rules')

# File uploader to accept Word documents
uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])
if uploaded_file is not None:
    # Read the document content
    document_content = read_docx(uploaded_file)
    # Show the document content (optional, could be removed for large documents)
    st.text_area("Document Content", value=document_content, height=300, disabled=True)
    
    # Input for rules on how to answer questions
    rules = st.text_area("Rules for answering questions",
                         value="The answer should be concise and to the point.",
                         height=100)
    
    # Input for asking questions
    question = st.text_input("Ask a question based on the document")
    
    if question:
        # Generate an answer using GPT-3
        answer = ask_gpt3(question, document_content, rules)
        st.write(answer)
