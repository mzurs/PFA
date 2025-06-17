from dataclasses import dataclass
import chainlit as cl


@dataclass
class UserInfo:
    """
    A class to represent user information.

    Attributes:
        name (str): The name of the user.
        age (int): The age of the user.
        occupation: str = ""
        monthly_income: float = 0.0
        savings: float = 0.0
        risk_tolerance: str = ""
    """

    name: str
    age: int
    occupation: str = ""
    monthly_income: float = 0.0
    savings: float = 0.0
    risk_tolerance: str = ""

    def to_context_message(self) -> list:
        """Convert user info to a list containing the system context message."""
        return [
            {
                "role": "system",
                "content": f"User Profile Information:\nName: {self.name}\ Age: {self.age}\nOccupation: {self.occupation}\nMonthly Income: ${self.monthly_income}\nSavings: ${self.savings}\nRisk Tolerance: {self.risk_tolerance}",
            }
        ]


async def ask_user_info() -> UserInfo:
    """
    Asks the user for their name and age, and returns them as a tuple.
    """

    # Basic personal information
    name_res = await cl.AskUserMessage(content="What is your name?", timeout=30).send()
    age_res = await cl.AskUserMessage(content="What is your age?", timeout=30).send()
    occupation_res = await cl.AskUserMessage(
        content="What is your occupation?", timeout=30
    ).send()

    # Financial information
    income_res = await cl.AskUserMessage(
        content="What is your monthly income?", timeout=30
    ).send()
    savings_res = await cl.AskUserMessage(
        content="How much do you have in savings?", timeout=30
    ).send()

    # Risk profile
    risk_res = await cl.AskUserMessage(
        content="What is your risk tolerance (conservative/moderate/aggressive)?",
        timeout=30,
    ).send()
    user = UserInfo(
        name=name_res["output"],
        age=int(age_res["output"]),
        occupation=occupation_res["output"],
        monthly_income=float(income_res["output"]),
        savings=float(savings_res["output"]),
        risk_tolerance=risk_res["output"],
    )

    return user
