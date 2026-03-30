from pydantic import BaseModel, Field
from typing import List 

class ResearchRequest(BaseModel):
    task : str = Field(
        ..., 
        description="The issue that the agents must investigate",
        json_schema_extra={"example": "Impact of AI on cybersecurity in 2026"})
    max_iterations : int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of steps that agents can take")
    
class FinalReport(BaseModel):
    title : str = Field(..., description="Professional title of the report")
    executive_summary: str = Field(..., description="Summary for managers")
    key_findings: str = Field(..., description="List of main findings (strings)")
    sources: str = Field(..., description="List of sources (strings)")
    conclusion: str = Field(..., description="Final recommendation")