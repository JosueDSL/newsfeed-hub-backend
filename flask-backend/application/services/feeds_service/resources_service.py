# Description: Service layer for resources

from application.models import Resource
from database import db

class ResourcesService:
    """
    A service class to interact with the resources in the database.
    """

    def insert_feed_resources(self, topics_models: list, feeds_data: list) -> list:
        """
        Insert feed resources into the database.

        Args:
            topics_models (list): The list of topic models.
            feeds_data (list): The list of feeds data.

        Returns:
            list: A list of newly created resource objects.
        """
        resources_models = []
        for data in feeds_data:
            topic_name = data['topic']
            topic_model = next((topic for topic in topics_models if topic.name == topic_name), None)
            if not topic_model:
                continue

            for item in data['data']['items']:
                
                # Extract the start and end year from the item data
                start_year = item.get('start_year', '')
                end_year = item.get('end_year', '')

                new_resource = Resource(
                    topic_id=topic_model.id,
                    title=item['title'],
                    date=f"{start_year} - {end_year}" if start_year and end_year else item.get('date', ''),
                    type=item.get('type', ''),
                    editorial=item.get('editorial', ''),
                    languages=','.join(item.get('language', []))
                )
                db.session.add(new_resource)
                resources_models.append(new_resource)

        db.session.commit()
        return resources_models