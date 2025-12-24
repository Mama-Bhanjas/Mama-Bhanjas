module disaster_truth_platform::truth_token {
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    /// The TRUTH token type
    public struct TRUTH_TOKEN has drop {}

    /// Initialize the token with a treasury cap for minting/burning
    fun init(witness: TRUTH_TOKEN, ctx: &mut TxContext) {
        let (treasury, metadata) = coin::create_currency(
            witness,
            6, // decimals
            b"TRUTH",
            b"Truth Token",
            b"Token for staking and rewards in Disaster Truth Platform",
            option::none(),
            ctx
        );
        
        // Transfer the treasury cap to the deployer for administrative control
        transfer::public_freeze_object(metadata);
        transfer::public_transfer(treasury, tx_context::sender(ctx));
    }

    /// Mint new TRUTH tokens (only the treasury owner can do this)
    public entry fun mint(
        treasury: &mut TreasuryCap<TRUTH_TOKEN>,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext
    ) {
        let coin = coin::mint(treasury, amount, ctx);
        transfer::public_transfer(coin, recipient);
    }

    /// Burn TRUTH tokens
    public entry fun burn(
        treasury: &mut TreasuryCap<TRUTH_TOKEN>,
        coin: Coin<TRUTH_TOKEN>
    ) {
        coin::burn(treasury, coin);
    }

    /// Get airdrop for new users (mint 50 tokens for testing)
    public entry fun claim_airdrop(
        treasury: &mut TreasuryCap<TRUTH_TOKEN>,
        ctx: &mut TxContext
    ) {
        let coin = coin::mint(treasury, 50_000000, ctx); // 50 tokens with 6 decimals
        transfer::public_transfer(coin, tx_context::sender(ctx));
    }
}
