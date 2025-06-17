from dataclasses import dataclass
import datetime
import random
from typing import cast
from src.agent_prompts import AGENT_INSTRUCTIONS_PROMPT
from agents import Runner, Agent, function_tool
import requests  # Replace http.client with requests
from src.config import model_config
from pydantic import BaseModel
import chainlit as cl
from src.user_info import UserInfo
import pandas as pd
from agents.run import RunConfig

advice_agent = Agent(
    name="You are a Personal Investment Advice, you recieve user personal information and you advice them whether to invest and how much to invest with respect to their savings!",
    instructions=AGENT_INSTRUCTIONS_PROMPT,
    model=model_config()[1],
)

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
    user_info: UserInfo = cast(UserInfo, cl.user_session.get("user_info"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    """Suggest an investment strategy based on user profile and Asset (ETH) past data."""
    result = Runner.run_sync(
        starting_agent=advice_agent,
        input=f"Given the  User Profile Information : {user_info}. Now suggest and give financial advice.",
        run_config=config,
    )

    return result.final_output



