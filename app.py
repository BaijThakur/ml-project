from dotenv import load_dotenv ## load all the env variable
load_dotenv()

import os
import PyPDF2
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    pdfreader=PyPDF2.PdfReader(uploaded_file)
    text=""
    for page_num in range(len(pdfreader.pages)):
        page = pdfreader.pages[page_num]
        text += page.extract_text()
        return text

##Prompt Template

input_prompt="""
Act Like a Highly Skilled Human Resource and Identify the resumes of candidates with the following attributes:
5 years of experience in Software Development, Data Science, Big Data Engineering.
Past experience or contributions to open-source projects.
Strong problem-solving skills evidenced by hackathons, side projects, unique implementations.
Educational background in Computer Science, Data Science, Engineering, or related fields
resume:{text}
description:{jd}

I want the response as percentae match of resume with JS and missing skills
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":"", "Candidate Name":""}}
"""


## Streamlit App
st.title("Advanced Resume Tracker")
st.text("SMART RESUME TRACKER")
jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload your resume", type="pdf",help="plesae upload the pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)


