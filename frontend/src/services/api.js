const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
console.log("Using API URL:", API_URL);

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
        const isFormData = data instanceof FormData;
        const endpoint = isFormData ? `${API_URL}/reports/upload/` : `${API_URL}/reports/`;
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: isFormData ? {} : {
                'Content-Type': 'application/json',
            },
            body: isFormData ? data : JSON.stringify(data),
        });
        if (!response.ok) throw new Error('Failed to submit report');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};

export const fetchRealtimeNews = async () => {
    try {
        const response = await fetch(`${API_URL}/news/realtime`);
        if (!response.ok) throw new Error('Failed to fetch realtime news');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return { success: false, data: [] };
    }
};
export const triggerIntelligenceSync = async () => {
    try {
        const response = await fetch(`${API_URL}/news/sync`); // We'll create this route in backend/app/routes/news.py
        if (!response.ok) throw new Error('Failed to trigger sync');
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
