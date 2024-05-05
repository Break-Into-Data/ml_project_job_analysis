from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class CompanyOverview(BaseModel):
    """
    A model for capturing key information about the company offering the job.
    
    Extract relevant details about the company from the job description, 
    including a brief overview of its industry and products, its mission and 
    values, size, and location(s).
    
    Focus on capturing the most salient points that give a well-rounded picture
    of the company and its culture.
    """

    about: Optional[str] = Field(
        None, 
        description="""Brief description of the company, its industry, products, services, 
                    and any notable achievements or differentiators"""
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
        description="""Geographic presence of the company, including headquarters, 
                    offices, and any remote work options"""
    )
    
    city: Optional[str] = Field(None, description="City where the company is located")
    
    state: Optional[str] = Field(None, description="State where the company is located")


class RoleSummary(BaseModel):
    """
    A model for capturing the key summary points about the job role.
    
    Extract the essential high-level details about the role from the job description,
    such as the job title, the team or department the role belongs to, the role type, 
    and any remote work options.
    
    Prioritize information that helps understand the overall scope and positioning 
    of the role within the company.
    """
    
    title: str = Field(..., description="Title of the job role")
    
    team_or_department: Optional[str] = Field(
        None,
        description="""Team, department, or business unit the role belongs to, 
                    including any collaborations with other teams"""
    )
    
    role_type: Optional[str] = Field(
        None,
        description="Type of role (full-time, part-time, contract, etc.)"
    )
    
    remote: Optional[str] = Field(
        None,
        description="Remote work options for the role (full, hybrid, none)"
    )

class ResponsibilitiesAndQualifications(BaseModel):
    """
    A model for capturing the key responsibilities, requirements, and preferred 
    qualifications for the job role.

    Extract the essential duties and expectations of the role, the mandatory 
    educational background and experience required, and any additional skills 
    or characteristics that are desirable but not strictly necessary.

    The goal is to provide a clear and comprehensive picture of what the role 
    entails and what qualifications the ideal candidate should possess.
    """

    responsibilities: List[str] = Field(
        description="""The core duties, tasks, and expectations of the role, encompassing 
                    areas such as metrics, theories, business understanding, product 
                    direction, systems, leadership, decision making, strategy, and 
                    collaboration, as described in the job description"""
    )

    required_qualifications: List[str] = Field(
        description="""The essential educational qualifications (e.g., Doctorate, 
                    Master's, Bachelor's degrees in specific fields) and years of 
                    relevant professional experience that are mandatory for the role, 
                    including any alternative acceptable combinations of education 
                    and experience, as specified in the job description"""
    )
    
    preferred_qualifications: List[str] = Field(
        description="""Any additional skills, experiences, characteristics, or domain 
                    expertise that are valuable for the role but not absolute 
                    requirements, such as proficiency with specific tools/technologies, 
                    relevant soft skills, problem solving abilities, and industry 
                    knowledge, as mentioned in the job description as preferred or 
                    nice-to-have qualifications"""
    )
    
class CompensationAndBenefits(BaseModel):
    """
    A model for capturing the compensation and benefits package for the job role.
    
    Extract details about the salary or pay range, bonus and equity compensation, 
    benefits, and perks from the job description.
    
    Aim to provide a comprehensive view of the total rewards offered for the role,
    including both monetary compensation and non-monetary benefits and perks.
    """
    
    salary_or_pay_range: Optional[str] = Field(
        None,
        description="""The salary range or hourly pay range for the role, including 
                    any specific numbers or bands mentioned in the job description"""
    )
    
    bonus_and_equity: Optional[str] = Field(
        None,
        description="""Any information about bonus compensation, such as signing bonuses, 
                    annual performance bonuses, or other incentives, as well as details 
                    about equity compensation like stock options or RSUs"""
    )
    
    benefits: Optional[List[str]] = Field(
        None,
        description="""A list of benefits offered for the role, such as health insurance, 
                    dental and vision coverage, retirement plans (401k, pension), paid 
                    time off (vacation, sick days, holidays), parental leave, and any 
                    other standard benefits mentioned in the job description"""
    )
    
    perks: Optional[List[str]] = Field(
        None,
        description="""A list of additional perks and amenities offered, such as free food 
                    or snacks, commuter benefits, wellness programs, learning and development 
                    stipends, employee discounts, or any other unique perks the company 
                    provides to its employees, as mentioned in the job description"""
    )

class JobDescription(BaseModel):
    """Extracted information from a job description."""
    company_overview: CompanyOverview
    role_summary: RoleSummary
    responsibilities_and_qualifications: ResponsibilitiesAndQualifications
    compensation_and_benefits: CompensationAndBenefits