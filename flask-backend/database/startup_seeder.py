# Description: This file contains the function that seeds the database with default roles.

# Import the User model
from application.models import User, Feed, Topic, Resource
from flask import current_app as app
from . import db
import random

class StartupSeeder:
    def __init__(self, app):
        self.app = app

    def seed(self):
        with self.app.app_context():
            # If there are no User in the database
            if User.query.count() == 0:
                # Add default User
                user = User(username='kiosko')
                user.password = 'kiosko'

                # Add the User to the session
                db.session.add(user)
                db.session.flush()  # Flush the changes to the database


            # If there are no Feeds in the database
            if Feed.query.count() == 0:
                # Add default Feeds
                feeds_to_add = [
                    Feed(user_id=user.id, name='Kiosko News Public', is_public=True),
                    Feed(user_id=user.id, name='Kiosko News Private', is_public=False)
                ]

                # Add the feeds to the session
                db.session.add_all(feeds_to_add)
                db.session.commit()


                # Set a list of topics to add to each feed
                topics_to_add = [
                    Topic(feed_id=feeds_to_add[0].id, name='Swimming'),
                    Topic(feed_id=feeds_to_add[0].id, name='Cycling'),
                    Topic(feed_id=feeds_to_add[0].id, name='Tennis'),
                    Topic(feed_id=feeds_to_add[0].id, name='Boxing'),
                    Topic(feed_id=feeds_to_add[0].id, name='Shooting'),
                    Topic(feed_id=feeds_to_add[1].id, name='Equestrian'),
                    Topic(feed_id=feeds_to_add[1].id, name='Jumping'),
                    Topic(feed_id=feeds_to_add[1].id, name='Sailing'),
                    Topic(feed_id=feeds_to_add[1].id, name='Rhythmic'),
                    Topic(feed_id=feeds_to_add[1].id, name='Gymnastics')
                ]

                # Bulk insert for efficiency
                db.session.add_all(topics_to_add)
                db.session.commit()

                """Artificially generate resources for each topic, to simulate a larger database
                   This approach ensures that the database is seeded with a large number of resources
                   even if any of the third party APIs are not available or the user has not added any resources manually.
                """

                # Sample data for resources
                titles = [
                    'The World of Sports', 'Breaking Records', 'Winning Strategies', 'The Future of Sports',
                    'Sports Illustrated', 'Champion Mindset', 'Athletic Life', 'Olympic Dreams', 
                    'Game Day Insights', 'Masters of the Game', 'Sports Legends', 'Victory Lap', 
                    'Athlete Spotlight', 'Game Changers', 'Sports Science', 'Beyond the Finish Line', 
                    'Inside the Arena', 'The Playbook', 'Sports Heroes', 'Winning Streak', 
                    'The Competitive Edge', 'Sports Revolution', 'Peak Performance', 'The Sports Journal', 
                    'Game On', 'The Athletic Tribune', 'Sports Pulse', 'The Winning Formula', 
                    'Sports Chronicles', 'The Sports Digest'
                ]

                types = ['Magazine', 'Journal', 'Article', 'Newspaper']
                editorials = ['Sports Weekly', 'Olympic Digest', 'Global Sports', 'Winning Edge']
                languages = ['English', 'Spanish', 'French']

                # Add resources to each topic
                for topic in topics_to_add:
                    resources_to_add = [
                        Resource(
                            topic_id=topic.id,
                            title=random.choice(titles),
                            date=random_date_range(),
                            type=random.choice(types),
                            editorial=random.choice(editorials),
                            languages=random.choice(languages)
                        )
                        for _ in range(50)
                    ]

                    # Bulk insert for efficiency
                    db.session.bulk_save_objects(resources_to_add)

                # Commit the changes to the database
                db.session.commit()

                app.logger.info('Database seeded successfully.')



# Function to generate a random date range like "1950 - 2024"
def random_date_range():
    start_year = random.randint(1950, 2016)  # Start year between 1950 and 2016
    end_year = random.randint(start_year, start_year + 8)  # End year within 8 years after start year
    return f"{start_year} - {end_year}"