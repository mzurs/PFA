from agents import Agent

from src.config import model_config
from src.prompts.agent_prompts import AGENT_INSTRUCTIONS_PROMPT


class PFA:
    """
    Personal Financial Assistant (PFA) application.
    This class encapsulates the main agent and its configuration for handling financial queries.
    """

    def __init__(self) -> None:
        self.agent = None

    def get_main_agent(self) -> Agent:
        """
        Returns the main agent for the Personal Financial Assistant application.
        This agent is configured with specific instructions and tools to assist users
        with their financial queries and tasks.
        """

        from src.tools.function_tools import FunctionTools

        tool = FunctionTools()
        agent: Agent = Agent(
            name="Personal Financial Assistant",
            instructions=AGENT_INSTRUCTIONS_PROMPT,
            model=model_config()[1],
            tools=[
                tool.random_number_tool,
                tool.fetch_current_price_tool,
                tool.fetch_latest_block,
                tool.convert_key_to_address,
                tool.send_transaction,
                # tool.get_balance,
                tool.get_balance_in_eth,
                tool.suggest_investment_tool,
                tool.list_asset_price_history_tool,
                tool.get_rpc_url,
                tool.get_private_key,
            ],
        )
        return agent
