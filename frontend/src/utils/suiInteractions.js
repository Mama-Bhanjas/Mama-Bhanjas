import { Transaction } from '@mysten/sui/transactions';
import { SUI_CONFIG, TRUTH_TOKEN_CONFIG } from './suiConfig';

/**
 * Claim airdrop of 50 TRUTH tokens
 */
export async function claimAirdrop(signAndExecuteTransaction) {
  const tx = new Transaction();
  
  tx.moveCall({
    target: `${SUI_CONFIG.PACKAGE_ID}::truth_token::claim_airdrop`,
    arguments: [
      tx.object(SUI_CONFIG.TREASURY_CAP),
    ],
  });

  // mutateAsync returns a promise directly
  const result = await signAndExecuteTransaction({
    transaction: tx,
  });
  
  console.log('Airdrop claimed successfully:', result);
  return result;
}

/**
 * Submit a disaster report with staked TRUTH tokens
 */
export async function submitReport(reportHash, truthCoinObject, signAndExecuteTransaction) {
  const tx = new Transaction();
  
  tx.moveCall({
    target: `${SUI_CONFIG.PACKAGE_ID}::disaster_report::submit_report`,
    arguments: [
      tx.object(SUI_CONFIG.REPORT_REGISTRY),
      tx.pure(Array.from(new TextEncoder().encode(reportHash))),
      tx.object(truthCoinObject),
      tx.object(SUI_CONFIG.CLOCK_OBJECT),
    ],
  });

  const result = await signAndExecuteTransaction({
    transaction: tx,
  });
  
  console.log('Report submitted successfully:', result);
  return result;
}

/**
 * Verify a report (admin only)
 */
export async function verifyReport(reportId, isValid, signAndExecuteTransaction) {
  const tx = new Transaction();
  
  tx.moveCall({
    target: `${SUI_CONFIG.PACKAGE_ID}::disaster_report::verify_report`,
    arguments: [
      tx.object(SUI_CONFIG.REPORT_REGISTRY),
      tx.object(SUI_CONFIG.TREASURY_CAP),
      tx.pure(reportId, 'u64'),
      tx.pure(isValid, 'bool'),
    ],
  });

  const result = await signAndExecuteTransaction({
    transaction: tx,
  });
  
  console.log('Report verified successfully:', result);
  return result;
}

/**
 * Get TRUTH token balance for an address
 */
export async function getTruthTokenBalance(suiClient, address) {
  try {
    const coins = await suiClient.getCoins({
      owner: address,
      coinType: `${SUI_CONFIG.PACKAGE_ID}::truth_token::TRUTH_TOKEN`,
    });

    const totalBalance = coins.data.reduce((sum, coin) => sum + BigInt(coin.balance), BigInt(0));
    return Number(totalBalance);
  } catch (error) {
    console.error('Error fetching TRUTH balance:', error);
    return 0;
  }
}

/**
 * Get a TRUTH coin object with at least the required amount
 */
export async function getTruthCoinObject(suiClient, address, requiredAmount = TRUTH_TOKEN_CONFIG.MIN_STAKE_AMOUNT) {
  try {
    const coins = await suiClient.getCoins({
      owner: address,
      coinType: `${SUI_CONFIG.PACKAGE_ID}::truth_token::TRUTH_TOKEN`,
    });

    // Find a coin with enough balance
    const suitableCoin = coins.data.find(coin => Number(coin.balance) >= requiredAmount);
    
    if (suitableCoin) {
      return suitableCoin.coinObjectId;
    }

    return null;
  } catch (error) {
    console.error('Error fetching TRUTH coin:', error);
    return null;
  }
}

/**
 * Fetch all reports from Sui blockchain using events
 */
export async function fetchReportsFromSui(suiClient) {
  try {
    // Query ReportSubmitted events
    const events = await suiClient.queryEvents({
      query: {
        MoveEventType: `${SUI_CONFIG.PACKAGE_ID}::disaster_report::ReportSubmitted`,
      },
      limit: 50,
      order: 'descending',
    });

    // Query ReportVerified events for status
    const verifiedEvents = await suiClient.queryEvents({
      query: {
        MoveEventType: `${SUI_CONFIG.PACKAGE_ID}::disaster_report::ReportVerified`,
      },
      limit: 50,
    });

    // Create a map of report statuses
    const statusMap = {};
    verifiedEvents.data.forEach(event => {
      const { report_id, status } = event.parsedJson;
      statusMap[report_id] = status;
    });

    // Map events to report objects
    const reports = events.data.map(event => {
      const { report_id, report_hash, reporter, timestamp } = event.parsedJson;
      
      return {
        id: report_id,
        hash: report_hash,
        reporter,
        timestamp: Number(timestamp),
        status: statusMap[report_id] || 0, // 0 = Pending, 1 = Verified, 2 = Rejected
        txDigest: event.id.txDigest,
      };
    });

    return reports;
  } catch (error) {
    console.error('Error fetching reports from Sui:', error);
    return [];
  }
}

/**
 * Get report count from contract
 */
export async function getReportCount(suiClient) {
  try {
    const tx = new Transaction();
    tx.moveCall({
      target: `${SUI_CONFIG.PACKAGE_ID}::disaster_report::get_report_count`,
      arguments: [tx.object(SUI_CONFIG.REPORT_REGISTRY)],
    });

    const result = await suiClient.devInspectTransactionBlock({
      sender: '0x0000000000000000000000000000000000000000000000000000000000000000',
      transactionBlock: tx,
    });

    if (result.results && result.results[0]) {
      const count = result.results[0].returnValues[0][0];
      return Number(count);
    }

    return 0;
  } catch (error) {
    console.error('Error getting report count:', error);
    return 0;
  }
}

/**
 * Create a SHA-256 hash of report content
 */
export async function hashReportContent(content, location) {
  const dataString = JSON.stringify({ content, location, timestamp: Date.now() });
  const encoder = new TextEncoder();
  const data = encoder.encode(dataString);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}
