# Sui Blockchain Deployment Configuration

## Deployed on Sui Testnet
**Deployment Date**: 2025-12-24
**Transaction Digest**: 21vRHi16FRAjD2zTriL6E15KAzm3CYMvq2r56CGPcvjK

## Important Object IDs

### Package ID
```
0x165f15bfefb05194683110786caac233221a2397c4b12cc9cd80a87ec78bbfbc
```
This is the main package containing both `disaster_report` and `truth_token` modules.

### TreasuryCap (TRUTH_TOKEN)
```
0x1ddbf7787d7f6e1e2473656793b5b6e53faea19e83ac9f792ad156b726fa068e
```
Use this to mint new TRUTH tokens or claim airdrops.
**Owner**: Your account (0x3bee6489eed940d1af5a9b202188dfd3995be9a86702eb8b09a06d9bf50706a0)

### ReportRegistry (Shared Object)
```
0x0b1f66e80c71310b10b1931eae67bb4c4aa2d124bd8bdd931e2ae20f9dbaa1c6
```
Use this for submitting and verifying disaster reports.
**Type**: Shared Object (accessible by all users)

## Frontend Environment Variables

Add these to your `frontend/.env.local`:

```env
NEXT_PUBLIC_SUI_PACKAGE_ID=0x165f15bfefb05194683110786caac233221a2397c4b12cc9cd80a87ec78bbfbc
NEXT_PUBLIC_SUI_TREASURY_CAP=0x1ddbf7787d7f6e1e2473656793b5b6e53faea19e83ac9f792ad156b726fa068e
NEXT_PUBLIC_SUI_REPORT_REGISTRY=0x0b1f66e80c71310b10b1931eae67bb4c4aa2d124bd8bdd931e2ae20f9dbaa1c6
NEXT_PUBLIC_SUI_NETWORK=testnet
```

## Quick Start Commands

### Claim Airdrop (50 TRUTH)
```bash
sui client call \
  --package 0x165f15bfefb05194683110786caac233221a2397c4b12cc9cd80a87ec78bbfbc \
  --module truth_token \
  --function claim_airdrop \
  --args 0x1ddbf7787d7f6e1e2473656793b5b6e53faea19e83ac9f792ad156b726fa068e \
  --gas-budget 10000000
```

### Submit Report (requires TRUTH coin)
```bash
sui client call \
  --package 0x165f15bfefb05194683110786caac233221a2397c4b12cc9cd80a87ec78bbfbc \
  --module disaster_report \
  --function submit_report \
  --args 0x0b1f66e80c71310b10b1931eae67bb4c4aa2d124bd8bdd931e2ae20f9dbaa1c6 "<REPORT_HASH>" <TRUTH_COIN_ID> 0x6 \
  --gas-budget 10000000
```

## Explorer Links

- **Package**: https://suiscan.xyz/testnet/object/0x165f15bfefb05194683110786caac233221a2397c4b12cc9cd80a87ec78bbfbc
- **Transaction**: https://suiscan.xyz/testnet/tx/21vRHi16FRAjD2zTriL6E15KAzm3CYMvq2r56CGPcvjK

## Gas Cost
- **Storage Cost**: 32.14 SUI
- **Computation Cost**: 0.001 SUI
- **Total**: ~32.16 SUI
