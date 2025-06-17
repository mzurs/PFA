from web3 import Web3
from agents import function_tool
import os
from dotenv import load_dotenv

rpc_url = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")


@function_tool
def fetch_latest_block():
    """Get the lastest block of Blockchain"""
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    return w3.eth.get_block_number()


@function_tool
def convert_key_to_address(private_key):
    """Converts a private key to an Ethereum address."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    account = w3.eth.account.from_key(private_key)
    return account.address


@function_tool
def get_balance():
    """Gets the balance of an Ethereum address in Wei."""
    address = "0xBE33a42b20274691C9AAA28f5E2533d16Ad7bc72"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    balance = w3.eth.get_balance(address)
    return balance


@function_tool
def get_balance_in_eth(address):
    """Gets the balance of an Ethereum address in Ether."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    address = "0xBE33a42b20274691C9AAA28f5E2533d16Ad7bc72"
    balance = w3.eth.get_balance(address)
    balance_in_eth = w3.from_wei(balance, "ether")
    return balance_in_eth


@function_tool
def send_transaction(to_address, amount_in_eth):
    """Sends a transaction from one address to another."""
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = w3.eth.account.from_key(private_key)
        from_address = account.address
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        nonce = w3.eth.get_transaction_count(from_address)
        gas_price = w3.eth.gas_price
        # Convert amount to Wei
        amount_in_wei = w3.to_wei(amount_in_eth, "ether")

        transaction = {
            "nonce": nonce,
            "to": to_address,
            "value": amount_in_wei,
            "gas": 21000,  # Standard gas limit for ETH transfer
            "gasPrice": gas_price,
        }

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        print(f"Signed Transaction : ", signed_txn)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return f"Transaction Hash: {tx_hash.hex()}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
