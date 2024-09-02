import streamlit as st
from main import CourseLangChain

@st.cache_resource
def initChain():
    return CourseLangChain()

st.title("🦜🔗 Langchain Quickstart App")

def generate(query):
    chain = initChain()
    for chunk in chain.chain.stream(query):
        yield chunk

def generate_response(input_text):
    st.write_stream(generate(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "我想修C語言，請幫我排課表")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)