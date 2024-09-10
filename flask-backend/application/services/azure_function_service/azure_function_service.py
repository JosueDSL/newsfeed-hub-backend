# Description: 
"""
    This file contains the AzureFunctionService class which is responsible 
        for handling the communication with the Azure Function service asynchronously.
"""

# Import the necessary modules
import httpx
from httpx import HTTPStatusError

class AzureFunctionService:
    """
    A service class to interact with the Azure Function service asynchronously.
    """
    def __init__(self, function_url):
        self.function_url = function_url

    async def fetch_data(self, topics: list):
        """
        Sends asynchronous request to the Azure Function with a list of topics.

        Args:
            topics (list): The list of topics to fetch.

        Returns:
            dict: The response from the Azure Function.
        """

        try:
            async with httpx.AsyncClient() as client:
                # Send the list of topics as JSON to the Azure Function
                response = await client.post(self.function_url, json={"topics": topics})

            # Check if the response was successful
            response.raise_for_status()

            # Return the JSON response
            return response.json()

        except HTTPStatusError as e:
            # Handle specific HTTP errors
            if e.response.status_code == 401:
                return {"error": "Unauthorized access. Please check your function key or credentials."}
            elif e.response.status_code == 404:
                return {"error": "The requested resource was not found."}
            else:
                return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}

        except Exception as e:
            # Handle other possible errors
            return {"error": f"An error occurred: {str(e)}"}
        
