from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Literal
from naptha_sdk.schemas import EnvironmentConfig

class FinancialState(BaseModel):
    """Represents current state of financial analysis"""
    workflow_stage: Optional[Literal["analysis", "research", "report"]] = None
    tickers: List[str] = Field(default_factory=list)
    financial_analysis: Dict[str, Any] = Field(default_factory=dict)
    market_research: Dict[str, Any] = Field(default_factory=dict)
    final_report: Optional[str] = None

class FinancialEnvironmentConfig(EnvironmentConfig):
    """Configuration for financial environment"""
    config_name: str
    environment_type: str = "financial"
    max_analyses: int = 10  # Maximum number of analyses to store
    analysis_retention_days: int = 30  # How long to keep analyses

class InputSchema(BaseModel):
    """Schema for environment inputs"""
    function_name: str
    function_input_data: Optional[Dict[str, Any]] = None