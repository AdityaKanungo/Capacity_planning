import streamlit as st
import openai
from docx import Document

def process_question(question, doc):
    # This function would contain the logic for processing the question
    # For now, it just returns a placeholder string
    return "This is where the answer would go"

openai.api_key = ''

def process_question(question, doc):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()


st.title('Word Document Interrogator')

uploaded_file = st.file_uploader("Choose a Word document", type="docx")
if uploaded_file is not None:
    doc = Document(uploaded_file)
    user_question = st.text_input("Ask a question based on the document")
    if user_question:
        answer = process_question(user_question, doc)
        st.write(answer)
