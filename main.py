import streamlit as st
from PIL import Image
import docx2txt
import base64
import re
import openai
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# Your OpenAI API key (replace with your actual key)
openai.api_key = ''

# Streamlit UI Configuration
st.set_page_config(page_title="SQL Query Generator", layout="wide")

## Header - Nav --------------------------

def get_image_as_data_url(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

def get_custom_html(data_url):
    with open("custom_styles.html", "r") as file:
        return file.read().replace("{data_url}", data_url)

data_url = get_image_as_data_url("header3.png")
custom_html = get_custom_html(data_url)
st.markdown(custom_html, unsafe_allow_html=True)
st.markdown(
    """
    <div class='navbar'>
        <p></p>
    </div>
    """,
    unsafe_allow_html=True,
)

def extract_text_from_multiple_docx(files):
    """Extract text from multiple DOCX files using docx2txt."""
    all_text = []
    for file in files:
        text = docx2txt.process(file)
        all_text.append(text)
    return "\n\n".join(all_text)  # Join all texts with a separator

def ask_gpt(question, document_text):
    messages = [
        {"role": "system", "content": f"""
        For these documents: {document_text}\n\n Answer this question based on the content of the documents only: {question}\n Answer:
        """
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message['content'].strip()

def generate_plot_code(question, document_text):
    messages = [
    {
        "role": "user",
        "content": f"""

        Create a python code to {question} in streamlit using potly express. Using the content of {document_text} only.
        Important!: Do not include ``` in the start and end of python code. e.g: Don't add "```python" or end with ```
        Don't add unnecessary code, eg: st.set_page_config(layout="wide")

        Initial python code to be updated

        # TODO import required dependencies
        # TODO Provide the plot
        # TODO Refer to examples below for each plot type and write similar code

        [EXAMPLE : SCATTER PLOT]

        import plotly.express as px
        fig = px.scatter(df, x="sepal_width", y="sepal_length")
        st.plotly_chart(fig)

        [EXAMPLE ENDS]
        
        [EXAMPLE 2 : BAR GRAPH ]

        For 2 variables:
        import plotly.express as px
        data_canada = px.data.gapminder().query("country == 'Canada'")
        fig = px.bar(data_canada, x='year', y='pop')
        st.plotly_chart(fig)

        For 3 variables:
        import plotly.express as px
        fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")
        st.plotly_chart(fig)


        [END OF EXAMPLE 2]

        [EXAMPLE 3: Historgram]

        # Convert the columns to their appropriate data types

        df['CompanyName'] = df['CompanyName'].astype(str)

        # Create the histogram for company name
        import plotly.express as px
        fig = px.histogram(df, x="CompanyName")
        st.plotly_chart(fig)
        [END OF EXAMPLE 3]

        DOUBEL CHECK : Output only the Python code for streamlit, no additional text.
        """
    }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    return response.choices[0].message['content'].strip()

# UI Components
image = Image.open('Capture.png')
st.image(image, width=200)

st.title('Word Document Interaction App')

# Using columns to layout the app
col1, col2 = st.columns([1, 2])  # Two columns of equal width

with col1:
    # File uploader and text input on the left column (col1)
    uploaded_files = st.file_uploader("Upload Word documents", type="docx", accept_multiple_files=True)
    if uploaded_files:
        # Extract the text from all documents
        document_text = extract_text_from_multiple_docx(uploaded_files)
        st.text_area("Combined Document Content", value=document_text, height=300, disabled=False)

with col2:

    # Displaying the answer on the right column (col2)
    question = st.text_input("Ask a question based on the documents")
    submit_button = st.button('Answer')  # Answer button

    if any(word in question for word in ["plot", "graph", "chart", "map", "bar", "line", "scatter", "tree", "heat", "pie"]):
        analysis_type = "Plot a graph"
    else:
        analysis_type = "Ask a question"

    if submit_button and question:
        # Process the question when the Answer button is clicked
        if analysis_type == "Ask a question":
            answer = ask_gpt(question, document_text)
            st.write(answer)
        elif analysis_type == "Plot a graph":
            python_code = generate_plot_code(question, document_text)
            if python_code:
                if "```" in python_code:
                    re.sub("```python","",python_code)
                    re.sub("```","",python_code)
                    st.code(python_code)
                    exec(python_code, globals())
                else:
                    st.code(python_code)
                    exec(python_code, globals())

    elif submit_button and not question:
        st.write("Please enter a question.")
