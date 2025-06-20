import os
from typing import cast

import chainlit as cl
from agents import Agent, Runner
from agents.run import RunConfig
from dotenv import load_dotenv

from src.config import model_config
from src.pfa import PFA
from src.user import User

load_dotenv()


@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", model_config()[0])

    await cl.Message(
        content="Hi! This is your Personal Financial Assistant. How can I help you today?"
    ).send()

    # Collect essential user information
    user_profile: User = User(
        name="",
        age=0,
        occupation="",
        monthly_income=0.00,
        savings=0.00,
        risk_tolerance="",
    )
    user_profile: User = await user_profile.set_user()

    agent: Agent = PFA().get_main_agent()
    load_dotenv()

    # Initialize chat history with user context
    chat_history = user_profile.to_context_message()  # This now returns a list
    cl.user_session.set("chat_history", chat_history)
    cl.user_session.set("private_key", user_profile.private_key)
    cl.user_session.set("rpc_url", os.getenv("RPC_URL"))
    cl.user_session.set("user_info", user_profile)
    cl.user_session.set("agent", agent)

    await cl.Message(
        content=f"Thank you {user_profile.name}! I now have enough information to provide personalized financial advice. You can now ask me anything related to your finances or investments!"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    user: User = cast(User, cl.user_session.get("user_info"))

    if not agent or not config or not user:
        msg.content = "Error: Agent or configuration or user info not found. Please start a new session."
        await msg.update()

        return await start()

    # Get the chat history, initialize if None
    history = cl.user_session.get("chat_history") or []

    # Add the new message to history
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        result = Runner.run_sync(starting_agent=agent, input=history, run_config=config)

        response_content = result.final_output

        # Update the thinking message
        msg.content = response_content
        await msg.update()

        # Add the response to history and update session
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")


@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")
