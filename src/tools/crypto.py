import chainlit as cl
from agents import function_tool
from web3 import Web3


class FunctionsTools_Crypto:
    """
    A class to encapsulate all function tools used in the Personal Financial Assistant application.
    This class is used to register function tools that can be called by the agent.
    """

    @function_tool
    def get_rpc_url() -> str:
        """Get the RPC URL from the user session."""
        return cl.user_session.get("rpc_url")

    @function_tool
    def get_private_key() -> str:
        """Get the private key from the user session."""
        return cl.user_session.get("private_key")

    @function_tool
    def fetch_latest_block():
        """Get the lastest block of Blockchain"""

        rpc_url: str = cl.user_session.get("rpc_url")
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        return w3.eth.get_block_number()

    @function_tool
    def convert_key_to_address() -> str:
        """Converts a private key to an Ethereum address."""
        rpc_url: str = cl.user_session.get("rpc_url")
        private_key: str = cl.user_session.get("private_key")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = w3.eth.account.from_key(private_key)
        return account.address

    # @function_tool
    # def get_balance():
    #     """
    #     - Gets the balance of an Ethereum in Wei.
    #     """
    #     rpc_url: str = cl.user_session.get("rpc_url")
    #     private_key: str = cl.user_session.get("private_key")
    #     w3 = Web3(Web3.HTTPProvider(rpc_url))
    #     balance = w3.eth.get_balance(private_key)
    #     return balance

    @function_tool
    def get_balance_in_eth():
        """
        - Gets the balance of an Ethereum in Ether.
        """
        rpc_url: str = cl.user_session.get("rpc_url")
        private_key: str = cl.user_session.get("private_key")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = w3.eth.account.from_key(private_key)
        address = account.address
        balance = w3.eth.get_balance(address)

        balance_in_eth = w3.from_wei(balance, "ether")
        return balance_in_eth

    @function_tool
    def send_transaction(to_address, amount_in_eth):
        """Sends a transaction from one address to another."""
        rpc_url: str = cl.user_session.get("rpc_url")
        private_key: str = cl.user_session.get("private_key")
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
            print("Signed Transaction : ", signed_txn)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            if tx_hash:
                return f'Transaction Hash: <a href="https://sepolia.etherscan.io/tx/{tx_hash.hex()}">{tx_hash.hex()}</a>'

            else:
                return f"Transaction Failed: {tx_hash}"

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
