from src.agent_prompts import AGENT_INSTRUCTIONS_PROMPT
from agents import Agent
from src.config import model_config
from src.crypto import (
    convert_key_to_address,
    fetch_latest_block,
    send_transaction,
    get_balance,
    get_balance_in_eth,
)
from src.function_tools import (
    fetch_current_price_tool,
    list_asset_price_history_tool,
    random_number_tool,
    suggest_investment_tool,
)


def get_main_agent() -> Agent:
    """
    Returns the main agent for the Personal Financial Assistant application.
    This agent is configured with specific instructions and tools to assist users
    with their financial queries and tasks.
    """
    agent: Agent = Agent(
        name="Personal Financial Assistant",
        instructions=AGENT_INSTRUCTIONS_PROMPT,
        model=model_config()[1],
        tools=[
            random_number_tool,
            fetch_current_price_tool,
            fetch_latest_block,
            convert_key_to_address,
            send_transaction,
            get_balance,
            get_balance_in_eth,
            suggest_investment_tool,
            list_asset_price_history_tool,
        ],
    )
    return agent
