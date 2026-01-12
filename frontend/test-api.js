// Test script to verify API connectivity
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

async function testBackendConnection() {
    console.log('='.repeat(60));
    console.log('TESTING BACKEND API CONNECTION');
    console.log('='.repeat(60));
    console.log(`API URL: ${API_URL}\n`);

    const tests = [
        { name: 'Root Endpoint', url: `${API_URL}/` },
        { name: 'Reports List', url: `${API_URL}/reports/` },
        { name: 'Realtime News', url: `${API_URL}/news/realtime` },
    ];

    for (const test of tests) {
        try {
            console.log(`Testing: ${test.name}`);
            console.log(`URL: ${test.url}`);
            
            const response = await fetch(test.url);
            const data = await response.json();
            
            console.log(`✅ SUCCESS (${response.status})`);
            console.log(`Response:`, JSON.stringify(data, null, 2).substring(0, 200));
            console.log('');
        } catch (error) {
            console.log(`❌ FAILED`);
            console.log(`Error: ${error.message}`);
            console.log('');
        }
    }
    
    console.log('='.repeat(60));
    console.log('TEST COMPLETE');
    console.log('='.repeat(60));
}

testBackendConnection();
