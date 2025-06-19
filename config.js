const config = {
    getApiEndpoint() {
        // Check if we're on localhost for development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000';
        }
        // For Vercel deployment - use the same domain as the frontend
        return window.location.origin;
    }
};