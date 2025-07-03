import os
import asyncio
from dotenv import load_dotenv

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction  # type: ignore
from solders.system_program import TransferParams, transfer
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price  # type: ignore
from spl.token.constants import WRAPPED_SOL_MINT, TOKEN_PROGRAM_ID
from spl.token.instructions import create_associated_token_account, sync_native, SyncNativeParams
from solana.rpc.types import TxOpts

LAMPORTS_PER_SOL = 1_000_000_000

async def wrap_sol(rpc_url: str, wallet: Keypair, wsol_pubkey: str, amount_sol: float):
    client = AsyncClient(rpc_url)
    instructions = [
        set_compute_unit_price(int(0.00001 * 1e9 * 25)),
        set_compute_unit_limit(40_000),
        create_associated_token_account(
            wallet.pubkey(), wallet.pubkey(), WRAPPED_SOL_MINT
        ),
        transfer(
            TransferParams(
                from_pubkey=wallet.pubkey(),
                to_pubkey=Pubkey.from_string(wsol_pubkey),
                lamports=int(LAMPORTS_PER_SOL * amount_sol),
            )
        ),
        sync_native(
            SyncNativeParams(
                program_id=Pubkey.from_string(TOKEN_PROGRAM_ID),
                account=Pubkey.from_string(wsol_pubkey)
            )
        ),
    ]

    blockhash_resp = await client.get_latest_blockhash("finalized")
    hb = blockhash_resp.value
    opts = TxOpts(
        skip_confirmation=True,
        skip_preflight=True,
        preflight_commitment="processed",
        last_valid_block_height=hb.last_valid_block_height
    )
    tx = Transaction.new_signed_with_payer(
        instructions, wallet.pubkey(), [wallet], hb.blockhash
    )
    resp = await client.send_raw_transaction(bytes(tx), opts)
    print(f"✅ Wrapped {amount_sol} SOL into WSOL. Transaction signature: {resp}")

async def main():
    load_dotenv()
    rpc = os.getenv("RPC_ADDRESS")
    key = os.getenv("PRIVATE_KEY")
    wsol = os.getenv("WSOL_ACCOUNT")
    amount = float(os.getenv("SOL_TO_WRAP", "1"))
    wallet = Keypair.from_base58_string(key)
    await wrap_sol(rpc, wallet, wsol, amount)

if __name__ == "__main__":
    asyncio.run(main())
