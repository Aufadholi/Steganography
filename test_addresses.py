#!/usr/bin/env python3
"""
Test Ethereum Address Validation
"""

import sys
import os
from pathlib import Path

# Add project path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from web3 import Web3

def validate_ethereum_address(address):
    """Validate Ethereum address format and checksum"""
    try:
        # Check basic format
        if not address.startswith('0x'):
            return False, "Address must start with 0x"
            
        if len(address) != 42:
            return False, f"Address length is {len(address)}, should be 42"
            
        # Check if it's a valid hex
        try:
            int(address[2:], 16)
        except ValueError:
            return False, "Address contains invalid hex characters"
            
        # Use Web3 to validate checksum
        w3 = Web3()
        if not w3.is_address(address):
            return False, "Invalid Ethereum address format"
            
        # Check checksum
        if not w3.is_checksum_address(address):
            correct_checksum = w3.to_checksum_address(address)
            return False, f"Invalid checksum. Correct: {correct_checksum}"
            
        return True, "Valid Ethereum address"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def main():
    """Test addresses"""
    print("🔍 Testing Ethereum Address Validation\n")
    
    test_addresses = [
        "0x03C779967c8581e092570e5d77832dFF7cF9ae27",  # Your address from .env
        "0x50E5786732143f349d55197388Db32d1b7DB8e5",   # Problem address
        "0x742d35Cc6671C0532925a3b8D4684dFBDE1e9C88",  # Valid test address
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",  # Valid test address
    ]
    
    for addr in test_addresses:
        is_valid, message = validate_ethereum_address(addr)
        status = "✅" if is_valid else "❌"
        print(f"{status} {addr}")
        print(f"   Result: {message}\n")

if __name__ == "__main__":
    main()