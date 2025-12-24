module disaster_truth_platform::disaster_report {
    use sui::object::{Self, UID};
    use sui::tx_context::{Self, TxContext};
    use sui::transfer;
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::balance::{Self, Balance};
    use sui::table::{Self, Table};
    use sui::event;
    use std::string::{Self, String};
    use disaster_truth_platform::truth_token::TRUTH_TOKEN;

    /// Errors
    const E_INSUFFICIENT_STAKE: u64 = 1;
    const E_REPORT_NOT_FOUND: u64 = 2;
    const E_ALREADY_VERIFIED: u64 = 3;
    const E_NOT_AUTHORIZED: u64 = 4;

    /// Report status
    const STATUS_PENDING: u8 = 0;
    const STATUS_VERIFIED: u8 = 1;
    const STATUS_REJECTED: u8 = 2;

    /// Configuration constants
    const MIN_STAKE_AMOUNT: u64 = 10_000000; // 10 TRUTH tokens (6 decimals)
    const REWARD_AMOUNT: u64 = 5_000000;     // 5 TRUTH tokens

    /// Main registry object
    public struct ReportRegistry has key {
        id: UID,
        reports: Table<u64, Report>,
        next_report_id: u64,
        admin: address,
        treasury: Balance<TRUTH_TOKEN>,
    }

    /// Report structure
    public struct Report has store {
        id: u64,
        report_hash: String,
        reporter: address,
        timestamp: u64,
        status: u8,
        stake: Balance<TRUTH_TOKEN>,
    }

    /// Events
    public struct ReportSubmitted has copy, drop {
        report_id: u64,
        report_hash: String,
        reporter: address,
        timestamp: u64,
    }

    public struct ReportVerified has copy, drop {
        report_id: u64,
        status: u8,
        reporter: address,
    }

    /// Initialize the module
    fun init(ctx: &mut TxContext) {
        let registry = ReportRegistry {
            id: object::new(ctx),
            reports: table::new(ctx),
            next_report_id: 0,
            admin: tx_context::sender(ctx),
            treasury: balance::zero(),
        };
        transfer::share_object(registry);
    }

    /// Submit a disaster report with staked tokens
    public entry fun submit_report(
        registry: &mut ReportRegistry,
        report_hash: vector<u8>,
        stake: Coin<TRUTH_TOKEN>,
        clock: &sui::clock::Clock,
        ctx: &mut TxContext
    ) {
        // Check minimum stake
        assert!(coin::value(&stake) >= MIN_STAKE_AMOUNT, E_INSUFFICIENT_STAKE);

        let report_id = registry.next_report_id;
        registry.next_report_id = report_id + 1;

        let report = Report {
            id: report_id,
            report_hash: string::utf8(report_hash),
            reporter: tx_context::sender(ctx),
            timestamp: sui::clock::timestamp_ms(clock),
            status: STATUS_PENDING,
            stake: coin::into_balance(stake),
        };

        table::add(&mut registry.reports, report_id, report);

        event::emit(ReportSubmitted {
            report_id,
            report_hash: string::utf8(report_hash),
            reporter: tx_context::sender(ctx),
            timestamp: sui::clock::timestamp_ms(clock),
        });
    }

    /// Verify a report (admin only)
    public entry fun verify_report(
        registry: &mut ReportRegistry,
        treasury: &mut TreasuryCap<TRUTH_TOKEN>,
        report_id: u64,
        is_valid: bool,
        ctx: &mut TxContext
    ) {
        // Only admin can verify
        assert!(tx_context::sender(ctx) == registry.admin, E_NOT_AUTHORIZED);
        
        // Check report exists
        assert!(table::contains(&registry.reports, report_id), E_REPORT_NOT_FOUND);
        
        let report = table::borrow_mut(&mut registry.reports, report_id);
        
        // Check not already verified
        assert!(report.status == STATUS_PENDING, E_ALREADY_VERIFIED);

        if (is_valid) {
            // Valid report: return stake + reward
            report.status = STATUS_VERIFIED;
            
            // Return stake
            let stake_amount = balance::value(&report.stake);
            let stake_coin = coin::from_balance(
                balance::withdraw_all(&mut report.stake),
                ctx
            );
            transfer::public_transfer(stake_coin, report.reporter);
            
            // Mint and send reward
            let reward = coin::mint(treasury, REWARD_AMOUNT, ctx);
            transfer::public_transfer(reward, report.reporter);
        } else {
            // Fake/Spam report: burn the stake
            report.status = STATUS_REJECTED;
            
            // Move stake to treasury (effectively burning it from circulation)
            let stake_amount = balance::withdraw_all(&mut report.stake);
            balance::join(&mut registry.treasury, stake_amount);
        };

        event::emit(ReportVerified {
            report_id,
            status: report.status,
            reporter: report.reporter,
        });
    }

    /// Get report count
    public fun get_report_count(registry: &ReportRegistry): u64 {
        registry.next_report_id
    }

    /// Update admin (admin only)
    public entry fun update_admin(
        registry: &mut ReportRegistry,
        new_admin: address,
        ctx: &mut TxContext
    ) {
        assert!(tx_context::sender(ctx) == registry.admin, E_NOT_AUTHORIZED);
        registry.admin = new_admin;
    }
}
