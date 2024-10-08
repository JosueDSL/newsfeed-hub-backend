# NewsFeed-Hub-Backend
---
## Overview

The NewsFeed-Hub-Backend is a Flask-based web application that provides a backend API for fetching and managing news data. It integrates with external data sources to gather news articles and organizes them into topics. The application also includes user authentication and authorization features, allowing users to securely access and manage their news feeds.

---

## Features
This project is a Flask-based web application designed to offer a range of features, including:

- User authentication and authorization using Flask-JWT-Extended and Flask-Login.
- Database migrations with Alembic and Flask-Migrate.
- Secure password handling via Flask-Bcrypt.
- Cross-origin resource sharing (CORS) enabled with Flask-CORS.
- ORM integration through Flask-SQLAlchemy.
- Modular code organization using Flask Blueprints for scalability.
- Class-based service-oriented architecture, using several design patterns.
---

## Requirements
To run the application, you will need the following dependencies:

- **Python 3.10+**
- **Docker (for containerized deployment)**
- **Flask** for the core framework.
- **SQLAlchemy** and **Alembic** for database ORM and migrations.
- **Flask-JWT-Extended** for authentication via JWT.
- **Flask-Login** for session management.

### Usage
To run the application locally, follow these steps:

Clone the repository:
```git
    git clone https://github.com/JosueDSL/newsfeed-hub-backend.git
    cd newsfeed-hub-backend
```

### Running the Project using a Container with Docker Compose
This project is recommended to be run directly from its container. To do so, navigate from the root folder to the `flask-backend` folder.

To run the container using Docker Compose, follow these steps:
---

1. **Navigate to the root project directory**:
    ```sh
    cd /newsfeed-hub-backend
    ```

    **Access `flask-backend` directory**:
    ```sh
    cd flask-backend
    ```

2. **Ensure Docker and Docker Compose are installed**:
    - [Install Docker](https://docs.docker.com/get-docker/)
    - [Install Docker Compose](https://docs.docker.com/compose/install/)

3. **Create a `.env` file**:
    - In the root directory of the project, create a `.env` file and add any necessary environment variables.
    Inside of the flask-backend directory you will see an example.env file [flask-backend/example.env](flask-backend/example.env)
    You can copy its contents to the `.env` file, the only thing it will be missing is gonna be the link to the azure functions app, 
    please refer to the .env file sent over to your email.

    ##### Example 
    ```env
        FLASK_APP=app.py
        FLASK_ENV=development
        FLASK_DEBUG=1
        SECRET_KEY=JsB9nESyzuOKajPa6gA6zuixRY5
        JWT_SECRET_KEY=LVy72N9j4X4woDlEs05Pne1uVZ4
        DEV_DATABASE_URL=sqlite:///newsfeed.db
        DEV_DATABASE_DOCKER_URL=sqlite:////app/newsfeed.db
        AZURE_FUNCTION_URL=https://enter-your-func-app-url.azurewebsites.net/api/function?
    ```

4. **Build and run the containers**:
    ```sh
    docker-compose up --build
    ```

5. **Access the application**:
    - Once the containers are up and running, you can access the application at `http://localhost:5000`.

6. **Stopping the containers**:
    - To stop the running containers, use:
    ```sh
    docker-compose down
    ```

By following these steps, you should be able to run the NewsFeed-Hub-Backend application in a containerized environment using Docker Compose.

### Running using a virtual enviroment both Flask and Azure Functions locally
To run the project entirely locally do as follows:

#### Run flask
1. **Create a virtual environment:**

```sh
    cd /newsfeed-hub-backend/flask-backend
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install the dependencies:**

```sh
    pip install -r requirements.txt
```

4. **Run the application:**

```sh
    flask run
```

#### Run azure function
**Prerequisites**
Install Node.js: Azure Functions Core Tools require Node.js. You can download and install it from nodejs.org.

Install Azure Functions Core Tools: You can install the Azure Functions Core Tools using npm (Node Package Manager).
```sh
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

Install Azure CLI: If you don't have the Azure CLI installed, you can download and install it from here.

- [Azure Functions Core Tools Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Azure Functions CLI Reference](https://docs.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference)

This should help you get your Azure Function running locally for development and testing purposes.

#### Steps to Run Azure Function Locally
5. Navigate to the Azure Function project directory:

```sh
    cd azure-functions
```

6. **Install dependencies**
Install dependencies: If your Azure Function project has a requirements.txt (for Python) or package.json (for Node.js), make sure to install the necessary dependencies.

In this case, this project uses node.js, run:
For Node.js:
```sh
    npm install
```

7. **Start the Azure Function:** Use the Azure Functions Core Tools to start your function app locally.
```sh
    npm install
```

#### Note: 
If you dont have the azure functions link, you can change your `.env` variable `"AZURE_FUNCTION_URL="` to:
```.env
    # Azure Function URL
    AZURE_FUNCTION_URL=http://localhost:7071/api/get-news-data?
```
Just update this variable in your .env, run azure functions in one terminal and your docker image in another, and done! 
You will be able to run this project 100% locally.


## Routes
The application provides the following API routes:

---
#### User Routes:

- POST `/user/register`: Register a new user.

#### Auth Routes: 

- POST `auth/login`: Authenticate a user and return a JWT.
- POST `auth/logout`: Get user profile information.
- GET  `auth/protected`: Protected route to test auth.

---
#### Feed Routes:

- POST   `/feeds/create-feed`: Create a new feed.
- PUT    `/feed/<int:feed_id>`: Update an existing feed.
- DELETE `/feed/<int:feed_id>`: Delete a feed.
- DELETE `/feed/topic/<int:feed_id>`: Delete a topic

---
#### Pagination Routes:

- GET `/feeds/list?page=1&per_page=10`: List Private Feeds.
- GET `/feeds/list-public?page=1&per_page=10`: List Public Feeds with Topic Filter.
- GET `/feeds/details/1`: List Feed Details.

## Models
The application uses SQLAlchemy for ORM. The primary models include:

---
- `User`: Represents a user in the system.
- `Feed`: Represents a news feed.
- `Topic`: Represents a topic within a feed.
- `Resource`: Represents a news article or resource within a topic.

Check out the Entity Relationship Diagram [Entity Relationship Diagram](https://drive.google.com/file/d/146H9AhHwSYPRlHLxqzI5GEOXQ0saj5ge/view?usp=sharing)
entity_relationship_diagram

![Entity Relationship Diagram](/flask-backend/database/assets/entity_relationship_diagram.webp)


## Project Structure
The project is organized into several modules and packages, including:

---
```markdown

├────── Root Directory 
│
│azure-functions/
││
│├── xcode/
││   └── node_modules/
│├── src_functions/
││   ├── function.json
││   └─────── get-new-data.js          # JavaScript file containing the Azure Function logic
│├── host.json                         # Configuration file for the function app host
│├── local.settings.json               # Local settings for running the function app locally
│└── package.json                      # Node.js project metadata and dependencies file─ host.json
│      
│flask-backend/    
││     
│├── application/      
││   ├── blueprints/                   # Contains the application's blueprints
││   │   ├── auth/     
││   │   │   └── routes.py             # Routes for user authentication
││   │   └── user/     
││   │   │   └── routes.py             # Routes for user management
││   │   └── feeds/    
││   │   │   └── routes.py             # Routes for feed management
││   │   └─── helper_methods.py        # Helper methods for the application
││   │   └── __init__.py               # Blueprint initialization 
││   │     
││   ├── models    
││   │   ├── feeds_models              # Models for feeds and topics
││   │   │   ├── __init__.py       
││   │   │   ├── feed.py       
││   │   │   ├── resource.py       
││   │   │   └── topic.py      
││   │   └── user_models               # Models for user management
││   │   │    ├── __init__.py      
││   │   │    └── user.py      
││   │   └── __init__.py               # Model initialization
││   │          
││   ├── services                      # Contains the application's services
││   │   ├── auth_service              # Services for user authentication
││   │   │   ├── __init__.py
││   │   │   └── auth_service.py
││   │   ├── azure_function_service    # Services for Azure Function integration
││   │   │   ├── __init__.py
││   │   │   └── azure_function_service.py 
││   │   ├── feeds_service             # Services for feed management
││   │   │   ├── __init__.py
││   │   │   ├── feed_data_handler.py  # Data handler for feeds (Assync API calls)
││   │   │   ├── feeds_service.py      # Feed service logic
││   │   │   ├── pagination_service.py # Pagination service logic
││   │   │   ├── resources_service.py  # Resource service logic
││   │   │   └── topics_service.py     # Topic service logic
││   │   │
││   │   │────── user_service
││   │   │    ├── __init__.py
││   │   │    ├── user_service.py      # User service logic
││   │   │   
││   │   ├────── base_validation_service.py  # Base class validation service
││   │
││   ├── __init__.py                   # Application initialization  **`Note: Core of the application`**
││   │── extensions.py                 # Flask extensions initialization
││   ├── database/                     # Database configuration and seeder
││       ├── __init__.py 
││       ├── database.py               # Database configuration
││       └── startup_seeder.py         # Seeder for initial data
││
││
│├── instance/    # Database instance folder (locally)
││      ├── newsfeed.db
││
││──────── migrations/                 # Database migrations 
││       ├── alembic.ini               # Alembic configuration
││       ├── env.py                    
││       ├── script.py.mako           
││       └── versions/                
││           
││
│├── tests/
││
│├── venv/                             # Virtual environment folder
││
│├── app.py                            # Application entry point
│├── app.log                           # Application log file
│├── config.py                         # Application configuration
│├── Dockerfile                        # Dockerfile for development
│├── DockerfileProd                    # Dockerfile for production (Example)
│├── docker-compose.yml                # Docker Compose configuration
│├── example.env                       # Example environment variables (copy to .env)
│├── env.py                            # Environment variables
│├── requirements.txt                  # Python dependencies
│├── newsfeed.db                       # SQLite database file (Docker volume)
│
├── .gitignore
├── README.md 
└── project_structure.md              # Project structure documentation - This file

```