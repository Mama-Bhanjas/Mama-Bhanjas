const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const fetchReports = async () => {
    try {
        const response = await fetch(`${API_URL}/reports/`);
        if (!response.ok) throw new Error('Failed to fetch reports');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
};

export const fetchSummaries = async () => {
    try {
        const response = await fetch(`${API_URL}/summaries/`);
        if (!response.ok) throw new Error('Failed to fetch summaries');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
}

export const submitReport = async (data) => {
    try {
        const response = await fetch(`${API_URL}/reports/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error('Failed to submit report');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
