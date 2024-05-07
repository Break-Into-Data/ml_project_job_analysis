from typing import List, Optional

from langchain.chains import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

from utils.job_desc_pydantic import JobDescription


# Set the LANGCHAIN_TRACING_V2 environment variable to 'true'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

# Set the LANGCHAIN_PROJECT environment variable to the desired project name
os.environ['LANGCHAIN_PROJECT'] = 'JobDescriptionProject'

load_dotenv()

def extract_desc_fields(raw_job_description, model_name="llama3-70b-8192"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at identifying key aspects of job descriptions. Your task is to extract important information from a raw job description and organize it into a structured format using the ResponsibilitiesAndQualifications class.

                    When parsing the job description, your goal is to capture as much relevant information as possible in the appropriate fields of the class. 
                    

                    The structured data you extract will be used for further analysis and insights downstream, so err on the side of including more information rather than less. The key is to make the unstructured job description data more organized and manageable while still retaining all the important details.
                """,
            ),
            ("human", "{text}"),
        ]
    )
    
    # llm = ChatAnthropic(model_name="claude-3-sonnet-20240229")
    llm = ChatGroq(model_name="llama3-70b-8192")
    # llm = ChatGroq(model_name="llama3-8b-8192")

    extractor = prompt | llm.with_structured_output(
        schema=JobDescription,
        method="function_calling",
        include_raw=False,
    )
    clean_description = extractor.invoke(raw_job_description)
    print(clean_description)
    return clean_description

