# Description: 
"""
    This file contains the AzureFunctionService class which is responsible 
        for handling the communication with the Azure Function service asynchronously.
"""

# Import the necessary modules
import httpx


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

        async with httpx.AsyncClient() as client:
            # Send the list of topics as JSON to the Azure Function
            response = await client.post(self.function_url, json={"topics": topics})

        # Check if the response was successful
        response.raise_for_status()

        # Return the JSON response
        return response.json()
