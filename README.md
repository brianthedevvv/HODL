# HODL Fee Distributor

![HODL Fee Distribution](https://i.imgur.com/gr3sQna.jpeg)

## Overview

HODL Fee Distributor is an automated Solana-based script that claims creator fees from Pump Fun and distributes them equally to all HODL token holders every 15 minutes. This addresses the limitation of Pump Fun's current fee-sharing model, which only rewards active traders rather than long-term holders.

## Problem Statement

Pump Fun's fee-sharing feature incentivizes swing trading over holding. Under their system:

- **Traders** who actively buy and sell (swing trade) accumulate trading volume and claim more fees
- **Holders** who purchase and hold get no rewards, despite being community supporters

This creates an unfair dynamic where the same amount of SOL locked in a position earns zero fees for holders, while a trader using the same SOL multiple times earns substantial rewards.

## Solution

The HODL Fee Distributor automatically:

1. **Collects** creator fees from Pump Fun every 15 minutes
2. **Identifies** all active HODL token holders on the blockchain
3. **Distributes** fees equally among all holders in a fair, transparent manner

This ensures that holders are rewarded for their support, creating a more inclusive and equitable reward system.

## Features

- ✅ **Automated Fee Collection** - Claims Pump Fun creator fees on a 15-minute cycle
- ✅ **Equal Distribution** - Divides fees equally among all HODL holders regardless of holding amount
- ✅ **Transparent** - All transactions are logged and verifiable on Solscan
- ✅ **Error Handling** - Includes retry logic and error reporting
- ✅ **Continuous Operation** - Runs as an always-on service with automatic restarts
- ✅ **Gas Optimization** - Maintains minimum balance to ensure uninterrupted operation

## How It Works

### Step 1: Claim Creator Fees
The script connects to Pump Fun's API and claims accumulated creator fees every 15 minutes.

```
Pump Fun API → Claim Creator Fees → Sign Transaction → Broadcast to Network
```

### Step 2: Fetch HODL Holders
The script queries the Solana blockchain to identify all current HODL token holders.

```
Solana RPC → getTokenLargestAccounts → Get all holder addresses
```

### Step 3: Calculate Distribution
Fees are divided equally among all holders.

```
Total Fees ÷ Number of Holders = Amount per Holder
```

### Step 4: Distribute to Holders
The script sends calculated amounts to each holder's wallet automatically.

```
For each holder: Send (Total Fees ÷ Holder Count) to holder address
```

### Step 5: Repeat
The entire process repeats automatically every 15 minutes.

## Installation

### Prerequisites

- Python 3.8+
- Solana wallet with some SOL for transaction fees
- A Solana RPC endpoint (free or paid)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/hodl-fee-distributor.git
cd hodl-fee-distributor
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create a configuration file** (`.env`):
```
PUBLIC_KEY=Your_Solana_Public_Key
PRIVATE_KEY=Your_Base58_Private_Key
RPC_ENDPOINT=https://api.mainnet-beta.solana.com/
HODL_MINT=Your_HODL_Token_Mint_Address
```

4. **Run the script:**
```bash
python hodl_fee_distributor.py
```

## Configuration

Edit these values in the script or environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `PUBLIC_KEY` | Your Solana wallet address | `SoL...` |
| `PRIVATE_KEY` | Your private key (base58 format) | `xxxxxx` |
| `RPC_ENDPOINT` | Solana RPC endpoint | `https://api.mainnet-beta.solana.com/` |
| `HODL_MINT` | HODL token mint address | `DfqJgvZXk...` |
| `DISTRIBUTION_INTERVAL` | Interval between distributions (seconds) | `900` (15 mins) |
| `PRIORITY_FEE` | Solana priority fee in SOL | `0.000001` |

## Output

The script logs all activity with timestamps and transaction links:

```
[2026-02-17 10:00:00] Claiming creator fees...
✓ Fees claimed successfully!
Transaction: https://solscan.io/tx/xxxxx

[2026-02-17 10:00:05] Fetching HODL holders...
Found 1,250 HODL holders

[2026-02-17 10:00:10] Distributing fees to 1,250 holders...
Distributing 0.0000450 SOL to each holder...
  Distributed to 10/1250 holders
  Distributed to 20/1250 holders
  ...
✓ Distribution complete! Successful: 1250, Failed: 0

Next distribution in 15 minutes...
```

## Security Considerations

⚠️ **IMPORTANT**: This script requires your private key. Always:

- Keep your private key secure and never commit it to version control
- Use environment variables or a secure secrets manager
- Run this on a secure, dedicated server
- Monitor transaction history regularly
- Keep SOL balance above minimum requirement (0.01 SOL recommended)

## Gas Costs

- **Fee Collection**: ~0.00005 SOL per transaction
- **Fee Distribution**: ~0.000005 SOL per holder per transaction
- **Total 15-min cost** (with 1,000 holders): ~0.005-0.01 SOL

Ensure your wallet maintains adequate balance to cover these costs.

## Troubleshooting

### "Insufficient balance for distribution"
The wallet doesn't have enough SOL. Send more SOL to your wallet.

### "Error claiming creator fees"
Check that your public key and Pump Fun API are accessible. Verify RPC endpoint is working.

### "Error fetching HODL holders"
Ensure the `HODL_MINT` address is correct and the token exists on the blockchain.

### "Transaction failed"
Check Solscan for transaction details. May be due to insufficient SOL or RPC issues.

## Roadmap

- [ ] Support for multiple fee collection sources
- [ ] Custom distribution intervals
- [ ] Holder weight-based distribution option
- [ ] Analytics dashboard
- [ ] Telegram/Discord notifications
- [ ] Database for transaction history

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Disclaimer

This script is provided as-is. The developers assume no responsibility for:
- Loss of funds due to misconfiguration
- Network failures or blockchain issues
- Changes to Pump Fun's API
- Smart contract vulnerabilities

Use at your own risk and always test in a development environment first.

---

**Built with ❤️ for the HODL community**
