# Project Structure

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
│
├── .gitignore
├── README.md 
└── project_structure.md              # Project structure documentation - This file

```