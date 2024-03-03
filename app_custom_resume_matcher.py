import os
import PyPDF2
import re
import spacy
import streamlit as st
from spacy.matcher import Matcher
# load pre-trained model
nlp = spacy.load('en_core_web_sm')
import json

extracted_text={}

def input_pdf_text(uploaded_file):
    pdfreader=PyPDF2.PdfReader(uploaded_file)
    text=""
    for page_num in range(len(pdfreader.pages)):
        page = pdfreader.pages[page_num]
        text += page.extract_text()
        return text

def get_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def get_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', num) for num in phone_numbers]

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
def extract_name(resume_text):
    nlp_text = nlp(resume_text) 
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]  
    matcher.add('NAME', [pattern], on_match=None)   
    matches = matcher(nlp_text)    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

#Extracting Skills
    
#Extracting Degree

## Streamlit App
st.title("Resume Parser")
st.text("Resume text parser")
#jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload your resume", type="pdf",help="plesae upload the pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        
        extracted_text['Name'] = extract_name(text)
        extracted_text['E-mail'] = get_email_addresses(text)
        extracted_text['Phone number'] = get_phone_numbers(text)
        

        # Serializing json 
        json_object = json.dumps(extracted_text, indent =8)
  
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
        
        st.subheader(json_object)

