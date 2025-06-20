import datetime
import random
from typing import cast

import chainlit as cl
import requests  # Replace http.client with requests
from agents import Agent, Runner, function_tool
from agents.run import RunConfig

from src.tools.crypto import FunctionsTools_Crypto
from src.prompts.agent_prompts import AGENT_INSTRUCTIONS_PROMPT
from src.config import model_config
from src.user import User

advice_agent = Agent(
    name="You are a Personal Investment Advice, you recieve user personal information and you advice them whether to invest and how much to invest with respect to their savings!",
    instructions=AGENT_INSTRUCTIONS_PROMPT,
    model=model_config()[1],
)


class FunctionTools(FunctionsTools_Crypto):
    """
    A class to encapsulate all function tools used in the Personal Financial Assistant application.
    This class is used to register function tools that can be called by the agent.
    """

    @function_tool
    def random_number_tool(max: int) -> int:
        """Return a random integer between 0 and the given maximum."""
        return random.randint(0, max)

    @function_tool
    def list_asset_price_history_tool(asset: str) -> str:
        """Fetch the price of a given asset."""
        with open("Binance_ETHUSDT_d.csv", "r") as file:
            list_prices = file.read()

        return list_prices

    @function_tool
    def fetch_current_price_tool(asset: str) -> str:
        """
        Fetch the most recent price of a given asset.
        Extract an asset name.
        """

        try:
            url = f"https://api.exchange.coinbase.com/products/{asset}-USDT/candles"
            params = {"start": datetime.datetime.now()}
            headers = {"Content-Type": "application/json"}

            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes

            data = response.json()
            if data and len(data) > 0:
                return data[0][1]  # Return the price from first candle
            return "Failed to fetch price"

        except requests.exceptions.RequestException as e:
            print(f"Error fetching price: {e}")
            return f"Error: {str(e)}"

    @function_tool
    def suggest_investment_tool(cls):
        user_info: User = cast(User, cl.user_session.get("user_info"))
        config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

        """Suggest an investment strategy based on user profile and Asset (ETH) past data."""
        result = Runner.run_sync(
            starting_agent=advice_agent,
            input=f"Given the  User Profile Information : {user_info}. Now suggest and give financial advice.",
            run_config=config,
        )

        return result.final_output
