const { app } = require('@azure/functions');
const axios = require('axios');

app.http('get-new-data', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        context.log(`Http function processed request for url "${request.url}"`);

        try {
            // Extract the 'topic' query parameter from the request
            const topic = request.query.get('topic') || await request.text() || 'general';
            
            // Call the Chronicling America API or any other API
            const apiUrl = `https://chroniclingamerica.loc.gov/search/titles/results/?terms=${topic}&format=json`;
            
            // Make the HTTP request to fetch news
            const response = await axios.get(apiUrl);
            
            // Log the response data
            context.log(`API response for topic "${topic}":`, response.data);

            // Return the API response data as the function output
            return {
                status: 200,
                body: response.data
            };

        } catch (error) {
            // Log any errors and return a failure message
            context.log.error('Error fetching data:', error.message);
            return {
                status: 500,
                body: 'Error fetching news data. Please try again later.'
            };
        }
    }
});
