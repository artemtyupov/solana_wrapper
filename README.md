# Solana SOL Wrapper

A Python tool for wrapping SOL into the SPL token (WSOL) via an asynchronous Solana RPC client.

## Overview

This script automates sending a specified amount of SOL to an associated token account and synchronizing the WSOL balance.  
Built on top of the [`solana-py`](https://github.com/michaelhly/solana-py), [`solders`](https://github.com/dfinity/solders) and [`spl-token`](https://github.com/solana-labs/solana-program-library) libraries.

## Requirements

- Python 3.8 or higher  
- Access to a Solana RPC endpoint (Mainnet, Devnet, or private node)  
- The following Python packages (see `requirements.txt`)

## Installation

```bash
git clone https://github.com/<YOUR_USERNAME>/solana-sol-wrapper.git
cd solana-sol-wrapper
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
