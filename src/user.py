from dataclasses import dataclass

import chainlit as cl

from src.config import is_valid_hex_key


@dataclass
class User:
    """
    A class to represent a single user information.

    Attributes:
        name (str): The name of the user.
        age (int): The age of the user.
        occupation: str = ""
        monthly_income: float = 0.0
        savings: float = 0.0
        risk_tolerance: str = ""
        private_key: str = ""
    """

    name: str = ""
    age: int = 0
    occupation: str = ""
    monthly_income: float = 0.00
    savings: float = 0.00
    risk_tolerance: str = ""
    private_key: str = ""

    @classmethod
    def to_context_message(self) -> list:
        """Convert user info to a list containing the system context message."""
        return [
            {
                "role": "user",
                "content": f"User Profile Information:\nName: {self.name}\nAge: {self.age}\nOccupation: {self.occupation}\nMonthly Income: ${self.monthly_income}\nSavings: ${self.savings}\nRisk Tolerance: {self.risk_tolerance}\nPrivate Key: {self.private_key}",
            }
        ]

    @classmethod
    async def set_user(self) -> "User":
        """
        Asks the user for their name and age, and returns them as a tuple.
        """
        files = None
        private_key = ""
        try:
            # Basic personal information
            name_res = await cl.AskUserMessage(
                content="What is your name?",
            ).send()

            age_res = await cl.AskUserMessage(
                content="What is your age?",
            ).send()

            occupation_res = await cl.AskUserMessage(
                content="What is your occupation?",
            ).send()

            # Financial information
            income_res = await cl.AskUserMessage(
                content="What is your monthly income?",
            ).send()
            savings_res = await cl.AskUserMessage(
                content="How much do you have in savings?",
            ).send()

            # Risk profile
            risk_res = await cl.AskUserMessage(
                content="What is your risk tolerance (conservative/moderate/aggressive)?",
            ).send()

            while files is None:
                files = await cl.AskFileMessage(
                    content="Please upload .txt file which contains only your private key.\n File contains PRIVATE_KEY=your-key-here and no space",
                    accept=["text/plain", ".txt"],
                    max_files=1,
                    max_size_mb=20,
                    timeout=180,
                ).send()

            if files:
                file = files[0]

                msg = cl.Message(content=f"Processing `{file.name}`...")
                await msg.send()
                with open(
                    file.path,
                    "r",
                ) as f:
                    for line in f:
                        if line.startswith("PRIVATE_KEY="):
                            private_key = line.strip().split("=", 1)[1]
                            print(private_key)
                            # msg = cl.Message(content=f"File content:\n{private_key}")
                            # await msg.send()

            self.name = name_res["output"]
            self.age = int(age_res["output"])
            self.occupation = occupation_res["output"]
            self.monthly_income = float(income_res["output"])
            self.savings = float(savings_res["output"])
            self.risk_tolerance = risk_res["output"]
            if is_valid_hex_key(private_key):
                msg = "Valid hexadecimal string."
                msg = cl.Message(content=msg)
                await msg.send()
            else:
                print(
                    "Invalid hexadecimal string. Please double-check that the private key you provided is a valid hexadecimal string."
                )
                msg = cl.Message(
                    content="Invalid hexadecimal string. Please double-check that the private key you provided is a valid hexadecimal string."
                )
                await msg.send()
            self.private_key = private_key
            if (
                not self.name
                or not self.age
                or not self.occupation
                or not self.monthly_income
                or not self.savings
                or not self.risk_tolerance
            ):
                await cl.Message(
                    content="All fields are required. Please try again."
                ).send()
                return await self.set_user()

            return self

        except ValueError as e:
            await cl.Message(content=f"Invalid input: {e}. Please try again.").send()
            return await self.set_user()  # Retry if input is invalid

    async def update_user(self) -> "User":
        """
        Asks the user for their updated information and returns the updated user object.
        """
        await cl.Message(content="Let's update your profile information.").send()
        return await self.set_user()
