const config = {
    getApiEndpoint() {
        if (window.location.hostname.includes('github.io')) {
            return 'https://your-aws-elastic-beanstalk-url.elasticbeanstalk.com';  // Replace with your AWS URL
        }
        return 'http://localhost:8000';
    }
}; 