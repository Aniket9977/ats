from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import fitz
import pdf2image
import google.generativeai as genai
api_key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)


def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_text = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()

        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are a seasoned Technical Human Resource Manager with deep expertise in matching candidates to technical roles. Your task is to thoroughly analyze the provided resume against the detailed job description. Evaluate the candidate's technical skills, relevant experience, education, and any industry certifications. Specifically, focus on:

1. **Technical Competencies:** Assess how well the candidate's technical skills align with the job requirements. Highlight any advanced skills or certifications that stand out, as well as any critical technical gaps.

2. **Professional Experience:** Evaluate the relevance and depth of the candidate's past experience in relation to the job. Consider the scope of their responsibilities, key achievements, and any leadership or team collaboration experience.

3. **Cultural Fit and Soft Skills:** Analyze the candidate's soft skills, such as communication, problem-solving, and adaptability. Consider how well their personality and work style might fit with the company culture.

4. **Potential for Growth:** Comment on the candidate's potential for growth within the role and the organization. Identify any areas where they may need additional training or support.

Provide a final recommendation on whether the candidate should advance to the next stage of the hiring process, along with specific reasons for your decision.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.write(response)
    else:
        st.write("Please uplaod the resume")
