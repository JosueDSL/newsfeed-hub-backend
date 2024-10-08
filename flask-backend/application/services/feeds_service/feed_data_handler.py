# Description: This file contains

# Required Libraries
from application.services.feeds_service import FeedsService, TopicService, ResourcesService
from application.services.azure_function_service import AzureFunctionService
from flask import current_app as app
from database import db
import asyncio


class FeedDataHandler:
    def __init__(self, payload: dict):
        # Initialize the services
        self.feeds_service = FeedsService()
        self.topic_service = TopicService()
        self.resources_service = ResourcesService()
        self.azure_function_service = AzureFunctionService(app.config['AZURE_FUNCTION_URL'])

        # Initialize the attributes
        self.feed_name = None
        self.is_public = None
        self.topics = None

        # Initialize the payload
        self.payload = payload


    async def process_request(self) -> dict:
        # Validate and initialize the payload
        self._validate_and_initialize_payload()

        # Fetch data for the topics from the third-party API asynchronously
        news_data = await self.azure_function_service.fetch_data(self.topics)

        # Validate and parse the response data
        found_topics, not_found_topics = self._validate_and_parse_response_data(news_data)

        # Raise an error if no data is found for the provided topics
        if not found_topics:
            not_found_topics_str = ", ".join(not_found_topics)
            raise ValueError(f"No data found for the provided topics: {not_found_topics_str}. Please insert another topic that exists.")

        # Save the data to the database asynchronously
        feed_model = await asyncio.to_thread(self.feeds_service.insert_feed, self.feed_name, self.is_public)


        try:
            # Insert the found topics into the database
            topics_models = await asyncio.gather(
                *[asyncio.to_thread(self.topic_service.insert_feed_topic, topic, feed_model.id) for topic in found_topics]
            )

        except ValueError as e:
            raise ValueError(f"Error occurred while inserting topics: {str(e)}")

        # Commit the transaction after adding all topics
        await asyncio.to_thread(self._commit_transaction, topics_models)

        # Insert the feed resources into the database
        resources_models = await asyncio.to_thread(self.resources_service.insert_feed_resources, topics_models, news_data)

        # Create a dictionary to hold the serialized topics and their resources
        serialized_topics = {}
        for topic_model in topics_models:
            # Get the resources associated with the current topic
            topic_resources = [resource for resource in resources_models if resource.topic_id == topic_model.id]
            
            # Serialize the resources
            serialized_resources = [resource.serialize() for resource in topic_resources]
            
            # Add the topic and its resources to the dictionary
            serialized_topics[topic_model.name] = serialized_resources

        # Return the response data
        response = {
            "feed_id": feed_model.id,
            "feed_name": feed_model.name,
            "is_public": feed_model.is_public,
            "topics": serialized_topics,
            "not_found_topics": not_found_topics
        }

        return response


    def _validate_and_initialize_payload(self) -> None:
        """
        Validate and initialize the payload data.

        Raises:
            ValueError: If the payload data is invalid.
        """

        # Check if the payload is a dictionary
        if not isinstance(self.payload, dict):
            raise ValueError("Invalid payload data: payload must be a dictionary")

        # Validate payload is not empty
        if not self.payload:
            raise ValueError("Invalid payload data: empty payload")

        # List of required fields and their expected types
        required_fields = {
            'feed_name': str,
            'is_public': bool,
            'topics': list
        }

        # Iterate over required fields and check if they are present in the payload
        for field, field_type in required_fields.items():
            if field not in self.payload:
                raise ValueError(f"Invalid payload data: missing {field}")
            elif not isinstance(self.payload[field], field_type):
                raise ValueError(f"Invalid payload data: {field} must be of type {field_type.__name__}")
            elif field != 'is_public' and not self.payload[field]:
                raise ValueError(f"Invalid payload data: {field} is empty")

        # Validate feed_name length
        feed_name = self.payload['feed_name']
        if len(feed_name) > 255:
            raise ValueError("Invalid payload data: feed_name must be less than 255 characters")
        elif len(feed_name) < 3:
            raise ValueError("Invalid payload data: feed_name must be at least 3 characters")

        # Additional validation for topics
        
        # Set global topic length limit
        MIN_TOPIC_LENGTH = 2
        MAX_TOPIC_LENGTH = 50


        topics = self.payload['topics']
        # if is not a list or is an empty list
        if len(topics) > 5:
            raise ValueError("Invalid payload data: topics list cannot contain more than 10 items")
        for topic in topics:
            if not isinstance(topic, str) or not topic.strip():
                raise ValueError("Invalid payload data: each topic must be a non-empty string")
            if len(topic) > MAX_TOPIC_LENGTH:
                raise ValueError(f"Invalid payload data: topic name must be less than {MAX_TOPIC_LENGTH} characters")
            elif len(topic) < MIN_TOPIC_LENGTH:
                raise ValueError(f"Invalid payload data: topic name must be at least {MIN_TOPIC_LENGTH} characters")

        # Ensure there are not duplicate topics
        if len(set(topics)) != len(topics):
            raise ValueError("Invalid payload data: duplicate topics are not allowed")

        # Initialize the attributes
        self.feed_name = feed_name
        self.is_public = self.payload['is_public']
        self.topics = topics


    def _validate_and_parse_response_data(self, response_data: list) -> tuple:
        """
        Validate and parse the response data from the third-party API.

        Args:
            response_data (list): The response data from the third-party API.

        Returns:
            tuple: A tuple containing the list of found topics and the list of not found topics.
        """

        # Check for an error in the response data
        if 'error' in response_data:
            raise ValueError(f"Error occurred while fetching data: {response_data['error']}")

        found_topics = []
        not_found_topics = []

        # Iterate over the response data
        for data in response_data:
            topic = data.get('topic')
            total_items = data.get('data', {}).get('totalItems', 0)
            
            if total_items > 0:
                found_topics.append(topic)
            else:
                not_found_topics.append(topic)

        return found_topics, not_found_topics



    def _commit_transaction(self, topics_models: list) -> None:
        """
        Commits the current session to the database.

        Args:
            topics_models (list): List of topic models to be added to the session.
        """
        # Add all topics to the session
        for topic in topics_models:
            db.session.add(topic)

        # Commit the transaction
        db.session.commit()