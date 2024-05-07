from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class CompanyOverview(BaseModel):
    """
    A model for capturing key information about the company offering the job.
    """

    about: Optional[str] = Field(
        None, 
        description="""Overview of the company, industry, products, services, and notable achievements"""
    )

    mission_and_values: Optional[str] = Field(
        None,
        description="""Company mission, vision, values, and culture, including commitments 
                    to diversity, inclusion, social responsibility, and work-life balance"""
    )
    
    size: Optional[str] = Field(
        None,
        description="Details about company size, such as number of employees")
    
    locations: Optional[str] = Field(
        None,
        description="""City, State where this position is based. """
    )

class RoleSummary(BaseModel):
    """
    A model for capturing the key summary points about the job role.
    
    Prioritize information that helps understand the overall scope and positioning 
    of the role within the company.
    """
    
    title: str = Field(..., description="Title of the job role")
    
    team_or_department: Optional[str] = Field(None,
        description="""Team, department, or business unit the role belongs to, 
                    including any collaborations with other teams"""
    )
    
    role_type: Optional[str] = Field(None,
        description="Type of role (full-time, part-time, contract, etc.)"
    )
    
    remote: Optional[str] = Field(None,
        description="Remote work options for the role (full, hybrid, none)"
    )

class ResponsibilitiesAndQualifications(BaseModel):
    """
    A model for capturing the key summary points about the job role.
    """

    responsibilities: List[str] = Field(None,
        description="""List of responsibilities, including tasks, duties, and expectations for the role"""
    )

    required_qualifications: List[str] = Field(None,
        description="""Essential educational qualifications and professional experience required for the role.
                    This may include, but not limited to, degrees, certifications, years of experience, technical skills, and domain knowledge.
                    """
    )
    
    preferred_qualifications: List[str] = Field(None,
        description="""Any additional qualifications that a candidate may possess to stand out or excel in the role.
                    This may include preferred skills, experience, certifications, or other attributes that are not essential but beneficial for the role.
                    """
    )
    
class CompensationAndBenefits(BaseModel):
    """
    A class for capturing details about the compensation and benefits offered for the role
    
    Aim to provide a comprehensive view of the total rewards offered for the role,
    including both monetary compensation and non-monetary benefits and perks.
    """
    
    salary_or_pay_range: Optional[str] = Field(None,
        
        description="""Salary range or hourly pay range for the role"""
    )
    
    bonus_and_equity: Optional[str] = Field(None,
        description="""Information about bonus and equity compensation"""
    )
    
    benefits_and_perks: Optional[List[str]] = Field(None,
        description="""List of benefits and perks offered for the role, such as insurance, retirement plans, and paid time off.
                        Can also include additional perks like free meals, wellness programs, learning stipends, etc."""
    )
    

class JobDescription(BaseModel):
    """Extracted information from a job description."""
    company_overview: CompanyOverview
    role_summary: RoleSummary
    responsibilities_and_qualifications: ResponsibilitiesAndQualifications
    compensation_and_benefits: CompensationAndBenefits