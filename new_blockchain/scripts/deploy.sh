#!/bin/bash

# Deployment script for Disaster Truth Platform on Sui

echo "========================================="
echo "Deploying Disaster Truth Platform to Sui"
echo "========================================="

# Check if Sui CLI is installed
if ! command -v sui &> /dev/null; then
    echo "Error: Sui CLI not found. Please install it first."
    echo "Visit: https://docs.sui.io/build/install"
    exit 1
fi

# Build the package
echo "Building Move package..."
sui move build

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# Publish to network (use --gas-budget flag)
echo "Publishing package..."
sui client publish --gas-budget 100000000

echo "========================================="
echo "Deployment complete!"
echo "========================================="
echo ""
echo "Save the following object IDs for later use:"
echo "1. Package ID"
echo "2. TreasuryCap object ID (for TRUTH_TOKEN)"
echo "3. ReportRegistry object ID"
echo ""
echo "You can find these in the transaction output above."
