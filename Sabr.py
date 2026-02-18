import requests
import time
import json
from datetime import datetime
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig
from solders.system_program import transfer, TransferParams
from solders.pubkey import Pubkey

# Configuration
PUBLIC_KEY = "Your public key here"
PRIVATE_KEY = "Your base 58 private key here"
RPC_ENDPOINT = "Your RPC Endpoint here - Eg: https://api.mainnet-beta.solana.com/"
Sabr_MINT = "Sabr token mint address here"
DISTRIBUTION_INTERVAL = 15 * 60  # 15 minutes in seconds
PRIORITY_FEE = 0.000001

def claim_creator_fees():
    """Claim creator fees from Pump Fun"""
    print(f"[{datetime.now()}] Claiming creator fees...")
    
    try:
        response = requests.post(url="https://pumpportal.fun/api/trade-local", data={
            "publicKey": PUBLIC_KEY,
            "action": "collectCreatorFee",
            "priorityFee": PRIORITY_FEE,
        })
        
        if response.status_code != 200:
            print(f"Error claiming fees: {response.status_code}")
            return None
        
        keypair = Keypair.from_base58_string(PRIVATE_KEY)
        tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [keypair])
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)
        
        response = requests.post(
            url=RPC_ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=SendVersionedTransaction(tx, config).to_json()
        )
        
        tx_signature = response.json()['result']
        print(f"✓ Fees claimed successfully!")
        print(f"Transaction: https://solscan.io/tx/{tx_signature}")
        return tx_signature
        
    except Exception as e:
        print(f"Error claiming creator fees: {str(e)}")
        return None

def get_Sabr_holders():
    """Get all Sabr token holders from blockchain"""
    print(f"[{datetime.now()}] Fetching Sabr holders...")
    
    try:
        # This fetches token accounts holding Sabr
        response = requests.post(
            url=RPC_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenLargestAccounts",
                "params": [Sabr_MINT]
            }
        )
        
        holders = response.json()['result']['value']
        print(f"Found {len(holders)} Sabr holders")
        return holders
        
    except Exception as e:
        print(f"Error fetching Sabr holders: {str(e)}")
        return []

def get_wallet_balance():
    """Get current wallet balance in SOL"""
    try:
        response = requests.post(
            url=RPC_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [PUBLIC_KEY]
            }
        )
        
        balance_lamports = response.json()['result']['value']
        balance_sol = balance_lamports / 1e9
        return balance_sol
        
    except Exception as e:
        print(f"Error fetching balance: {str(e)}")
        return 0

def distribute_fees_to_holders(holders, total_amount_sol):
    """Distribute fees equally to all Sabr holders"""
    print(f"[{datetime.now()}] Distributing fees to {len(holders)} holders...")
    
    if not holders or total_amount_sol <= 0:
        print("No holders or insufficient balance to distribute")
        return
    
    try:
        amount_per_holder = total_amount_sol / len(holders)
        amount_per_holder_lamports = int(amount_per_holder * 1e9)
        
        # Set minimum to cover transaction fees
        if amount_per_holder_lamports < 5000:  # Minimum 0.000005 SOL per transaction
            print(f"Amount per holder too small: {amount_per_holder} SOL")
            return
        
        keypair = Keypair.from_base58_string(PRIVATE_KEY)
        successful_transfers = 0
        failed_transfers = 0
        
        print(f"Distributing {amount_per_holder:.9f} SOL to each holder...")
        
        for i, holder in enumerate(holders):
            try:
                recipient_pubkey = Pubkey(holder['address'])
                
                # Create transfer instruction
                transfer_params = TransferParams(
                    from_pubkey=keypair.pubkey(),
                    to_pubkey=recipient_pubkey,
                    lamports=amount_per_holder_lamports
                )
                transfer_instruction = transfer(transfer_params)
                
                # Build and send transaction
                response = requests.post(
                    url=RPC_ENDPOINT,
                    headers={"Content-Type": "application/json"},
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "sendTransaction",
                        "params": [transfer_instruction]
                    }
                )
                
                if 'result' in response.json():
                    successful_transfers += 1
                    if (i + 1) % 10 == 0:
                        print(f"  Distributed to {i + 1}/{len(holders)} holders")
                else:
                    failed_transfers += 1
                    
            except Exception as e:
                failed_transfers += 1
                print(f"Error transferring to holder {i}: {str(e)}")
        
        print(f"✓ Distribution complete! Successful: {successful_transfers}, Failed: {failed_transfers}")
        
    except Exception as e:
        print(f"Error distributing fees: {str(e)}")

def main():
    """Main loop that runs every 15 minutes"""
    print("=" * 60)
    print("Sabr Fee Distributor Started")
    print("=" * 60)
    print(f"Wallet: {PUBLIC_KEY}")
    print(f"Distribution Interval: {DISTRIBUTION_INTERVAL // 60} minutes")
    print("=" * 60)
    
    while True:
        try:
            # Step 1: Claim creator fees
            claim_creator_fees()
            
            # Wait a bit for the transaction to settle
            time.sleep(5)
            
            # Step 2: Get wallet balance
            balance = get_wallet_balance()
            print(f"Current balance: {balance:.9f} SOL")
            
            # Step 3: Get Sabr holders
            holders = get_Sabr_holders()
            
            # Step 4: Distribute fees (keep minimum for next cycle)
            if balance > 0.01:  # Keep 0.01 SOL for transaction fees
                distribution_amount = balance - 0.01
                distribute_fees_to_holders(holders, distribution_amount)
            else:
                print("Insufficient balance for distribution")
            
            # Wait for the next cycle
            print(f"\nNext distribution in {DISTRIBUTION_INTERVAL // 60} minutes...")
            print("-" * 60)
            time.sleep(DISTRIBUTION_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\nDistributor stopped by user")
            break
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            print(f"Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()
