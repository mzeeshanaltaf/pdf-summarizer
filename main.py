from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from util import *
import os
from dotenv import load_dotenv

# Initialize streamlit app
page_title = "PDF Summarizer"
page_icon = "📝"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")


if "app_activation" not in st.session_state:
    st.session_state.app_activation = False

load_dotenv()

# --- MAIN PAGE CONFIGURATION ---
st.title(page_title)
st.write(':blue[***Effortless Summaries at Your Fingertips 📄✨***]')
st.write("Transform lengthy PDF documents into concise, easy-to-read summaries with this advanced summarization tool. "
         "Whether it's a research paper, report, or e-book, this application extracts the key points 📚, saving you "
         "time ⏳ and effort 💼 while ensuring you capture the essential information.")

# Configure the sidebar
st.sidebar.title("Configuration")
ai_company = sidebar_select_ai_company()
if ai_company == 'OpenAI':
    api_key = sidebar_api_key_configuration()
    llm = ChatOpenAI(openai_api_key=api_key)
elif ai_company == 'Groq':
    groq_api_key = sidebar_groq_api_key_configuration()
    model = sidebar_groq_model_selection()
    llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)


summarize_technique = sidebar_summarization_techniques()

st.subheader("Upload PDF")
uploaded_file = st.file_uploader("Upload PDF File", type=['pdf'], accept_multiple_files=False,
                                 label_visibility='collapsed', disabled=not st.session_state.app_activation)
if uploaded_file is not None:
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())

    summarize = st.button("Summarize", type="primary")
    st.subheader('Summary:')

    if summarize:
        with st.spinner(":blue[Summarizing ...]"):
            summarize = summarize_pdf(llm, temp_file, summarize_technique)
            st.write(summarize)
            os.remove(temp_file)
