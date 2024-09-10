# Azure Functions Overview

The azure-functions/ folder in this project houses the logic for managing Azure Functions, which are essential for handling external API requests asynchronously and offloading this work from the main Flask application. Using Azure Functions ensures that the system remains highly scalable, as each function can scale independently, responding to demand without overloading the Flask backend. This allows the Flask application to focus on core responsibilities like user management and JWT handling, while Azure Functions manage external API requests.

**The folder structure is as follows:**

```markdown
azure-functions/
│
├── .vscode/                              # Contains Visual Studio Code configuration files.
├── node_modules/                         # Contains project dependencies for the Node.js function app.
├── src_functions/                        # Folder where the function logic is stored.
│   ├── function.json                     # Configuration for the individual Azure Function.
│   ├── get-news-data.js                  # JavaScript file containing the logic for fetching news data from an external API.
├── host.json                             # Host-level configuration for Azure Functions runtime.
├── local.settings.json                   # Local settings for running Azure Functions on your development environment.
├── package.json                          # Node.js project metadata, including dependencies.
├── package-lock.json                     # Version-lock file for Node.js dependencies.

```

## Why Use Azure Functions in This Way?

- Asynchronous API Calls: Azure Functions allow us to make asynchronous requests to external APIs without blocking the main Flask application. By offloading these requests, the Flask app can handle more user requests concurrently, improving performance and reducing response times.
- Scalability: Azure Functions scale automatically based on the number of incoming requests. This is especially useful when dealing with high-traffic environments or a burst of API requests.
- Separation of Concerns: Offloading external API calls to Azure Functions separates concerns, allowing Flask to focus on core logic like user authentication and database interactions. This results in cleaner architecture and easier debugging.
- Cost-Efficiency: Azure Functions only run when triggered, meaning you only pay for the time that they are actively processing requests. This serverless model can significantly reduce operational costs in cloud environments.

### Key Files in Azure Functions

`src_functions/get-news-data.js`:
The main file responsible for fetching news data based on user input. This function takes a POST request, processes the provided topics, and fetches news articles from the Chronicling America Newsfeed API.

### Explanation of the Key Components:

1. **Azure Functions App Setup:**
    The function is defined using Azure Functions' Node.js SDK (@azure/functions), where app.http creates an HTTP trigger to listen for incoming requests. The authLevel: 'function' parameter specifies that the function requires a function key to be accessed, ensuring security and avoiding api abuse.

2. Topics Handling:
    The request body is expected to contain a topics array (e.g., ["politics", "economy"]). If no topics are provided, a default value of ['general'] is used.

3. Asynchronous Data Fetching:
    For each topic, an asynchronous call is made to the Chronicling America API to fetch news articles related to the topic. Axios is used for making the HTTP requests. This setup ensures that all the requests for different topics happen concurrently, minimizing the time needed to fetch data.

4. Promise.all for Concurrency:
    The Promise.all() method is used to wait for all asynchronous requests to complete before the function proceeds. This ensures that the response only goes out once all data has been retrieved, avoiding partial data return issues.

5. Response Formatting:
    The fetched data is formatted into a response object containing the topic and the corresponding news articles. This object is then sent back as the HTTP response.

6. Error Handling:
    A try-catch block ensures that any errors during the API requests are logged and handled properly. In case of failure, the function returns a 500 status code along with an error message in the response body.

#### Example Usage:
A client could send the following POST request to this function to get news data on specific topics:

```json
POST /api/get-news-data
{
    "topics": ["swimming", "shooting"]
}
```

**Response:** The function would return news articles related to "technology" and "sports" topics fetched from the Chronicling America API.