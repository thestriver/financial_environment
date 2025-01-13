#!/usr/bin/env python
from naptha_sdk.modules.environment import Environment
from naptha_sdk.schemas import EnvironmentRunInput
from typing import Dict, List, Any, Optional
from naptha_sdk.utils import get_logger
from financial_environment.schemas import FinancialState, FinancialEnvironmentConfig, InputSchema

logger = get_logger(__name__)

class FinancialEnvironment(Environment):
    """Environment for sequential financial analysis.
    
    This environment maintains the state of financial analyses performed by multiple agents:
    - Data Analyst: Performs financial metric analysis
    - Market Researcher: Conducts market research
    
    The environment tracks:
    - Current workflow stage (analysis/research/report)
    - Stock tickers being analyzed
    - Financial analysis results
    - Market research findings 
    - Final generated reports
    """
    
    def __init__(self, config: FinancialEnvironmentConfig):
        """Initialize environment with configuration settings.
        
        Args:
            config: Configuration specifying max analyses and retention period
        """
        self.config = config
        self.state = FinancialState()

    def get_global_state(self) -> Dict[str, Any]:
        """Get the current state of all financial analyses.
        
        Returns a dictionary containing:
        - Current workflow stage
        - List of tickers being analyzed
        - Completed financial analyses
        - Market research results
        - Generated final reports
        """
        return self.state.dict()

    def reset(self):
        """Reset the environment to initial state.
        
        Clears:
        - Current workflow stage
        - List of tickers
        - All financial analyses
        - All market research
        - All final reports
        """
        self.state = FinancialState()

    def close(self):
        """Clean up any environment resources.
        
        Currently a no-op as no cleanup is needed, but included for:
        - Future extensibility
        - Conforming to environment interface
        - Proper resource management
        """
        pass

def create_environment(module_run):
    """Create a new instance of FinancialEnvironment.
    
    Args:
        module_run: Contains deployment configuration
        
    Returns:
        Initialized FinancialEnvironment instance
    """
    config = FinancialEnvironmentConfig(**module_run.deployment.config)
    return FinancialEnvironment(config)

def run(module_run: EnvironmentRunInput):
    """Main entry point for environment execution.
    
    Args:
        module_run: Contains function name and input data
        
    Returns:
        Result of the called environment function
        
    Raises:
        Exception: If any error occurs during execution
    """
    try:
        env = create_environment(module_run)
        method = getattr(env, module_run.inputs.function_name)
        
        if module_run.inputs.function_input_data:
            return method(**module_run.inputs.function_input_data)
        return method()
        
    except Exception as e:
        logger.error(f"Error in environment run: {e}")
        raise

if __name__ == "__main__":
    """Example usage of the financial environment.
    
    Demonstrates:
    1. Loading environment deployments
    2. Creating an environment run input
    3. Getting global state
    """
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import load_environment_deployments
    
    naptha = Naptha()
    
    # Load environment configuration
    environment_deployments = load_environment_deployments(
        "financial_environment/configs/environment_deployments.json",
        config_schema=FinancialEnvironmentConfig()
    )
    
    # Create example run input
    module_run = EnvironmentRunInput(
        inputs=InputSchema(function_name="get_global_state"),
        deployment=environment_deployments[0],
        consumer_id=naptha.user.id
    )

    # Execute and print results
    response = run(module_run)
    print(response)