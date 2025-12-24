# Disaster Truth Platform - Sui Blockchain

## Quick Start

This directory contains the Sui Move implementation of the Disaster Truth Platform blockchain layer.

## What's Inside

- `sources/truth_token.move` - TRUTH token (Coin) implementation
- `sources/disaster_report.move` - Report submission and verification logic
- `scripts/deploy.sh` - Deployment script (Linux/Mac)
- `scripts/deploy.ps1` - Deployment script (Windows)
- `Move.toml` - Package configuration

## Prerequisites

Install Sui CLI: https://docs.sui.io/build/install

## Quick Deploy

```bash
# Build
sui move build

# Publish
sui client publish --gas-budget 100000000
```

## Documentation

See the full usage guide in the artifacts directory for detailed instructions on:
- Setup and deployment
- Submitting reports
- Verifying reports
- Frontend integration
- Testing workflow

## Features

✅ Truth Token (TRUTH) - ERC20-equivalent on Sui
✅ Staking mechanism (10 TRUTH per report)
✅ Verification with rewards (+5 TRUTH for valid)
✅ Slashing for fake reports (-10 TRUTH burned)
✅ Airdrop function for new users (50 TRUTH)
✅ Admin controls for verification
