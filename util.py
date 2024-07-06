from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st

summarize_approach_dic = {'Map Reduce': 'map_reduce', 'Stuff': 'stuff', 'Refine': 'refine'}


def sidebar_select_ai_company():
    st.sidebar.subheader("Select Company")
    ai_company = st.sidebar.selectbox('Select the AI Company', ('OpenAI', 'Groq'), label_visibility="collapsed")
    return ai_company


# Function for API configuration at sidebar
def sidebar_api_key_configuration():
    st.sidebar.subheader("API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password",
                                    help='Get API Key from: https://platform.openai.com/api-keys')
    if api_key == '':
        st.sidebar.warning('Enter the API Key 🗝️')
        st.session_state.app_activation = False
    elif api_key.startswith('sk-') and ((len(api_key) == 51) or (len(api_key) == 56)):
        st.sidebar.success('Lets Proceed!', icon='️👉')
        st.session_state.app_activation = True
    else:
        st.sidebar.warning('Please enter the correct API Key 🗝️!', icon='⚠️')
        st.session_state.app_activation = False
    return api_key


def sidebar_groq_api_key_configuration():
    st.sidebar.subheader("API Key")
    groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password",
                                         help='Get Groq API Key from: https://console.groq.com/keys')
    if groq_api_key == '':
        st.sidebar.warning('Enter Groq API Key 🗝️')
        st.session_state.app_activation = False
    elif groq_api_key.startswith('gsk_') and (len(groq_api_key) == 56):
        st.sidebar.success('Lets Proceed!', icon='️👉')
        st.session_state.app_activation = True
    else:
        st.sidebar.warning('Please enter the correct API Key 🗝️!', icon='⚠️')
        st.session_state.app_activation = False
    return groq_api_key


def sidebar_groq_model_selection():
    st.sidebar.subheader("Model Selection")
    model = st.sidebar.selectbox('Select the Model', ('Llama3-70b-8192', 'Mixtral-8x7b-32768',
                                                      'Gemma2-9b-it'), label_visibility="collapsed")
    return model


def sidebar_summarization_techniques():
    st.sidebar.subheader('Summarization Technique')
    option = st.sidebar.selectbox('Summarization Techniques', ['Map Reduce', 'Refine', 'Stuff'],
                                  label_visibility='collapsed')

    return summarize_approach_dic[option]


def summarize_pdf(llm, pdf_file_path, summarize_technique):

    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type=summarize_technique)
    summary = chain.invoke(docs)
    return summary['output_text']
