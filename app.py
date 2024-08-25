from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import fitz
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Debug print statements
        print("Input Text:", input_text)
        print("PDF Content:", pdf_content[:200])  # Print first 200 chars for brevity
        print("Prompt:", prompt)
        
        response = model.generate_content([input_text, pdf_content, prompt])
        print("API Response:", response)  # Debug print for API response

        return response.text
    except Exception as e:
        print(f"Error in generating content: {e}")
        return "Error in generating content."

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
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are a seasoned Technical Human Resource Manager with deep expertise in matching candidates to technical roles. Your task is to thoroughly analyze the provided resume against the detailed job description. Evaluate the candidate's technical skills, relevant experience, education, and any industry certifications. Specifically, focus on:

1. **Technical Competencies:** Assess how well the candidate's technical skills align with the job requirements. Highlight any advanced skills or certifications that stand out, as well as any critical technical gaps.

2. **Professional Experience:** Evaluate the relevance and depth of the candidate's past experience in relation to the job. Consider the scope of their responsibilities, key achievements, and any leadership or team collaboration experience.

3. **Cultural Fit and Soft Skills:** Analyze the candidate's soft skills, such as communication, problem-solving, and adaptability. Consider how well their personality and work style might fit with the company culture.

4. **Potential for Growth:** Comment on the candidate's potential for growth within the role and the organization. Identify any areas where they may need additional training or support.
5. **Give the ats score of the resume out of 100 , you can take a bit long to calculate the accurate score

Provide a final recommendation on whether the candidate should advance to the next stage of the hiring process, along with specific reasons for your decision.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage, and then keywords missing, and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.write(response)
    else:
        st.write("Please upload the resume")
