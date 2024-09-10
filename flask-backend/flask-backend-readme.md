# Flask Backend Overview

This section outlines the structure and functionality of the **Flask backend** that serves as the core API for user authentication, feed management, and integration with external services like Azure Functions.

The **Flask** backend is responsible for managing user sessions, handling database operations, interacting with external APIs, and providing secure JWT-based authentication. This modular architecture ensures scalability, maintainability, and separation of concerns. Below is a breakdown of the main components:

## Project Structure

```markdown
flask-backend/
├── application/                                # Core of the application containing blueprints, models, and services
│   ├── blueprints/                             # Contains the application's blueprints for routing
│   │   ├── auth/               
│   │   │   └── routes.py                       # Routes for user authentication (login, registration)
│   │   ├── user/               
│   │   │   └── routes.py                       # Routes for user management (profile, password update)
│   │   ├── feeds/              
│   │   │   └── routes.py                       # Routes for feed management (fetching and displaying feeds)
│   │   └── helper_methods.py                   # Contains helper functions like error handling
│   │   └── __init__.py                         # Initializes the blueprints for the application
│   ├── models/                                 # Data models for interacting with the database
│   │   ├── feeds_models                        # Models related to feeds and topics
│   │   │   ├── feed.py                         # Model representing individual feeds
│   │   │   ├── resource.py                     # Model representing feed resources
│   │   │   └── topic.py                        # Model representing topics
│   │   ├── user_models                         # Models for user management
│   │   │   ├── user.py                         # User model (handles password hashing, validation)
│   │   └── __init__.py                         # Initializes models and associations
│   ├── services/                               # Business logic and services layer for the application
│   │   ├── auth_service/
│   │   │   └── auth_service.py                 # Logic for user authentication (login, JWT handling)
│   │   ├── azure_function_service/
│   │   │   └── azure_function_service.py       # Service for integrating with Azure Functions (for async API requests)
│   │   ├── feeds_service/
│   │   │   ├── feed_data_handler.py            # Handles asynchronous API calls for fetching feed data
│   │   │   └── feeds_service.py                # Feed service logic (business logic for feeds)
│   │   ├── user_service/
│   │   │   └── user_service.py                 # User service logic (managing user profiles, updates)
│   │   ├── base_validation_service.py          # Base validation logic for consistent input validation
│   └── __init__.py                             # Application initialization, setting up services, extensions
│   ├── extensions.py                           # Initializes Flask extensions (e.g., SQLAlchemy, JWT, Flask-Cors)
│   ├── database/                               # Database configuration and migrations
│   │   ├── database.py                         # Database connection and setup using SQLAlchemy
│   │   └── startup_seeder.py                   # Initial data seeder for database population
├── instance/                                   # Instance folder containing database files (SQLite)
│   ├── newsfeed.db                             # SQLite database for local development
├── migrations/                                 # Database migration files generated using Alembic
│   ├── alembic.ini                             # Alembic configuration for database migrations
│   ├── env.py                                  # Alembic environment file for handling migrations
│   └── versions/                               # Migration versions for tracking changes to the database
├── app.py                                      # Main application entry point (starts the Flask application)
├── config.py                                   # Configuration file (environment variables, secrets, database URIs)
├── Dockerfile                                  # Dockerfile for containerizing the application (development)
├── DockerfileProd                              # Dockerfile for production environment (optional, example setup)
├── docker-compose.yml                          # Docker Compose file for setting up the Flask app with all dependencies
├── example.env                                 # Example environment variables file (can be copied to .env)
├── requirements.txt                            # Python dependencies file
```


### Key Components

1. **application/**:
    - This is the core directory containing all the business logic, routing, and models.
    - **blueprints/**: This folder contains route handlers for various sections of the application.
        - **auth/routes.py**: Manages user authentication (login, registration).
        - **user/routes.py**: Manages user-related actions (profile management).
        - **feeds/routes.py**: Handles API requests for fetching and displaying feeds.
        - **helper_methods.py**: Contains reusable methods, like centralized error handling.
    - **models/**: Contains the database models representing the user, feed, resource, and topic entities.
        - **user_models/user.py**: The User model handles user data storage and authentication (password hashing, JWT validation).
        - **feeds_models/**: Manages the structure of feeds and topics within the database.
    - **services/**: Contains the core business logic, separated from the routing to ensure scalability and maintainability.
        - **auth_service.py**: Implements user authentication services (login, JWT token generation).
        - **azure_function_service.py**: Handles communication with Azure Functions to fetch data asynchronously.
        - **feeds_service.py**: Implements feed retrieval and management logic.
        - **user_service.py**: Provides logic for managing user data.

2. **app.py**:
    - This file contains the entry point for running the Flask application. It imports the `create_app` function from the `application` package and starts the web server&#8203;:contentReference[oaicite:0]{index=0}.

3. **config.py**:
    - Configuration file that loads environment variables and sets up important configurations for the Flask app, such as the `SECRET_KEY`, `JWT` settings, and database URIs. It supports both local development and Docker-based setups&#8203;:contentReference[oaicite:1]{index=1}.

4. **database/**:
    - Contains database configuration, startup data seeder, and database initialization logic using SQLAlchemy.

5. **migrations/**:
    - Contains all Alembic migration files to track changes made to the database schema over time.

6. **requirements.txt**:
    - Lists the Python dependencies necessary to run the application, including Flask, SQLAlchemy, JWT, and other required libraries&#8203;:contentReference[oaicite:2]{index=2}.

7. **Dockerfile**:
    - The `Dockerfile` sets up the Flask environment inside a Docker container for development and testing purposes.
    
8. **docker-compose.yml**:
    - The Docker Compose configuration brings up the Flask backend along with any dependencies (like a database) in a containerized environment for development.

9. **.env/example.env**:
    - Example environment variables file to define important configuration details such as `SECRET_KEY`, `JWT_SECRET_KEY`, and `DATABASE_URL`.

---

This structure ensures that the **Flask** backend is modular, scalable, and easy to maintain. Each part of the application is isolated, making it simple to extend or modify specific functionalities (like adding new routes or models). Additionally, by integrating external services like **Azure Functions**, the backend can offload heavy or time-consuming tasks, ensuring high performance and scalability.

# IMPORTANT NOTE

The `application` directory **`__init__`** is the core of the Flask backend, containing the blueprints, models, services, and other essential components. This structure ensures that the application logic is organized and separated based on functionality, making it easier to maintain and scale the application.

```markdown
│├── application/
││   │
││   └─── __init__.py  # Application initialization  **`Note: Core of the application`**
```

## Config.py

The `config.py` file is responsible for loading environment variables and setting up configurations for the Flask application. It includes settings like the `SECRET_KEY

Inside the `application/__init__.py` you can pass two diferent configurations to the app, one for containerized development (Docker) and another for local development, it was set by default to use the Docker configuration, but you can change it just by passing the desired configuration class. 

at __init__.py:

```python

def create_app():

    # Import the configuration classes from the config module
    from config import (
        DevelopmentConfig,
        DevelopmentDockerConfig,
        # ProductionConfig,          # Another config class examples, just for common usage reference:
        # QAConfig
    )
    # Create an instance of the Flask application
    app = Flask(__name__)


    """
        NOTE: Change the configuration class to match the desired environment.
        Options:
        - DevelopmentConfig: For local development
        - DevelopmentDockerConfig: For Docker development

        Example:
        app.config.from_object(DevelopmentConfig)  # Use this for local development
        app.config.from_object(DevelopmentDockerConfig)  # Use this for Docker development
    """

    # Load the configuration from the config.py file
    app.config.from_object(DevelopmentDockerConfig) # Default configuration for Docker development

```

Here are some key reasons for using this structure:
- **Modularity**: The application is divided into distinct components (blueprints, models, services) that can be developed and tested independently.

- **Scalability**: The modular design allows for easy scaling of the application by adding new components or extending existing ones.

- **Separation of Concerns**: Each component has a specific responsibility, ensuring that the codebase is organized and easy to understand.