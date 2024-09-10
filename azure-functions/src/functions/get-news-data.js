const { app } = require('@azure/functions');
const axios = require('axios');

app.http('get-news-data', {
    methods: ['POST'],
    authLevel: 'function',          // Require a function key to access this endpoint, making it private and secure
    handler: async (request, context) => {
        context.log(`Http function processed request for url "${request.url}"`);

        try {
            // Extract the 'topics' array from the request body, if present
            const body = await request.json();
            const topics = body?.topics || ['general'];

            // Fetch results for all topics concurrently
            const promises = topics.map(async (topic) => {
                const apiUrl = `https://chroniclingamerica.loc.gov/search/titles/results/?terms=${topic}&format=json`;
                const response = await axios.get(apiUrl);
                return { topic, data: response.data };
            });

            // Wait for all promises to resolve
            const results = await Promise.all(promises);

            // Return the combined results
            return {
                status: 200,
                body: JSON.stringify(results),
                headers: {
                    'Content-Type': 'application/json'
                }
            };

        } catch (error) {
            context.log.error('Error fetching data:', error.message);
            return {
                status: 500,
                body: JSON.stringify({ error: 'Error fetching news data. Please try again later.' }),
                headers: {
                    'Content-Type': 'application/json'
                }
            };
        }
    }
});
