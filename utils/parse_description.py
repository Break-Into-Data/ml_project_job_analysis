from typing import List, Optional

from langchain.chains import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from utils.job_desc_pydantic import JobDescription

load_dotenv()



def extract_desc_fields(raw_job_description):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at identifying key aspects of job descriptions. Your task is to extract important information from a raw job description and organize it into a structured format using the ResponsibilitiesAndQualifications class.

                    When parsing the job description, your goal is to capture as much relevant information as possible in the appropriate fields of the class. This includes:

                    1. All key responsibilities and duties of the role, covering the full range of tasks and expectations.
                    2. The required educational qualifications and years of experience, including different acceptable combinations.
                    3. Any additional preferred skills, experiences, and characteristics that are desirable for the role.

                    Avoid summarizing or paraphrasing the information. Instead, extract the details as closely as possible to how they appear in the original job description. The aim is to organize and structure the raw data, not to condense or interpret it.

                    Some specific things to look out for:
                    - Responsibilities related to metrics, theories, business understanding, product direction, systems, leadership, decision making, strategy, and collaboration
                    - Required degrees (Doctorate, Master's, Bachelor's) in relevant fields, along with the corresponding years of experience
                    - Preferred qualifications like years of coding experience, soft skills, problem solving abilities, and domain expertise

                    If any of these details are missing from the job description, simply omit them from the output rather than trying to infer or fill in the gaps.

                    The structured data you extract will be used for further analysis and insights downstream, so err on the side of including more information rather than less. The key is to make the unstructured job description data more organized and manageable while still retaining all the important details.
                """,
            ),
            ("human", "{text}"),
        ]
    )
    
    llm = ChatGroq(model_name="llama3-70b-8192")

    extractor = prompt | llm.with_structured_output(
        schema=JobDescription,
        method="function_calling",
        include_raw=False,
    )
    
    return extractor.invoke(raw_job_description)

