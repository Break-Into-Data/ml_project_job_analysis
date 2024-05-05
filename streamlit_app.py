from dotenv import load_dotenv
import os
import streamlit as st
import time

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from utils import parse_description


# Setting up the environment variables for LangSmith tracing
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Resume_Project'

st.set_page_config(layout="wide")

st.title("Job Description Parser")

col1, col2 = st.columns([1,6])

with col1:
    st.image("images/jobDetailExtractor3part.png", use_column_width=True)

with col2:
    st.write("""
    Welcome to the Job Description Parser, a revolutionary tool designed to extract structured information from job descriptions using the magic of advanced Language Models (LLMs)! 🪄📄
    
    Our goal is to build a comprehensive database of job descriptions for various data-related positions, including Data Scientist 🔬, Data Engineer ⚙️, Data Analyst 📈, Machine Learning Engineer 🤖, and more! 💼 But we're not just collecting job postings – we're taking it to the next level! Our cutting-edge LLM will parse each job description and extract key information, giving you unparalleled insights into what skills, experiences, and qualities are most sought-after in the industry. 🔍
    
    We've designed a robust system using Pydantic models to capture and structure the most important aspects of each job description, including company overview, role summary, responsibilities and qualifications, and compensation and benefits. 💰
    
    In the near future, we'll be adding even more powerful features to help you land your dream data job, such as automatically categorizing job descriptions based on key characteristics, providing personalized resume suggestions based on your target roles, and offering insider tips and strategies for acing data job interviews. 🔮
    
    Upload a job description, select your models, and watch the magic happen. 🎩✨ Let's unlock the full potential of LLMs together and make job description parsing a breeze! 😎
    """)
    
llm_dict = {
    "GPT 3.5 turbo": ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    "Anthropic Sonnet": ChatAnthropic(model_name="claude-3-sonnet-20240229"),
    "Llama 3 8b": ChatGroq(model_name="llama3-8b-8192"),
    "Llama 3 70b": ChatGroq(model_name="llama3-70b-8192"),
    "Gemma 7b": ChatGroq(model_name="gemma-7b-it"),
    "Mixtral 8x7b": ChatGroq(model_name="mixtral-8x7b-32768"),
    # "Gemini 1.5 Pro": ChatGoogleGenerativeAI(model_name="gemini-1.5-pro-latest"),
}

col1, col2 = st.columns(2)

with col1:
    job_description = st.text_area("Enter the job description", height=3000)
    extract_button = st.button("Extract Fields from Description")

if extract_button and job_description:
    with col2:
        start_time = time.time()
        extracted_fields = parse_description.extract_desc_fields(job_description)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(f"Extraction completed in {elapsed_time:.2f} seconds")
        
        try:
            if extracted_fields.company_overview:
                st.write("## Company Overview")
                st.write(extracted_fields.company_overview.about)
                st.write(extracted_fields.company_overview.mission_and_values)
                st.write(f"Size: {extracted_fields.company_overview.size}")
                st.write(f"Locations: {extracted_fields.company_overview.locations}")
                st.write(f"City: {extracted_fields.company_overview.city}")
                st.write(f"State: {extracted_fields.company_overview.state}")

            if extracted_fields.role_summary:
                st.write("## Role Summary")
                st.write(f"Title: {extracted_fields.role_summary.title}")
                st.write(f"Team or Department: {extracted_fields.role_summary.team_or_department}")
                st.write(f"Role Type: {extracted_fields.role_summary.role_type}")
                st.write(f"Remote: {extracted_fields.role_summary.remote}")

            if extracted_fields.responsibilities_and_qualifications:
                st.write("## Responsibilities and Qualifications")
                st.write("### Responsibilities")
                for responsibility in extracted_fields.responsibilities_and_qualifications.responsibilities:
                    st.write(f"- {responsibility}")

                st.write("### Required Qualifications")
                for qualification in extracted_fields.responsibilities_and_qualifications.required_qualifications:
                    st.write(f"- {qualification}")

                st.write("### Preferred Qualifications")
                for qualification in extracted_fields.responsibilities_and_qualifications.preferred_qualifications:
                    st.write(f"- {qualification}")

            if extracted_fields.compensation_and_benefits:
                st.write("## Compensation and Benefits")
                st.write(f"Salary or Pay Range: {extracted_fields.compensation_and_benefits.salary_or_pay_range}")
                st.write(f"Bonus and Equity: {extracted_fields.compensation_and_benefits.bonus_and_equity}")
                st.write("### Benefits")
                for benefit in extracted_fields.compensation_and_benefits.benefits:
                    st.write(f"- {benefit}")
                st.write("### Perks")
                for perk in extracted_fields.compensation_and_benefits.perks:
                    st.write(f"- {perk}")

        except Exception as e:
            st.write(f"An error occurred: {e}")