azure-functions/
│
├── xcode/
│   └── node_modules/
├── src_functions/
│   ├── function.json
│   └── get-new-data.js
├── host.json
├── local.settings.json
└── package.json

flask-backend/
│
├── application/
│   ├── blueprints/
│   │   ├── auth/
│   │   │   └── routes.py
│   │   └── user/
│   │  
│   │       ├── __init__.py
│   │       ├── helper_methods.py
│   │       └── routes.py
│   ├── models
│   │   ├── feeds_models
│   │   │   ├── __init__.py
│   │   │   ├── feed.py
│   │   │   ├── resource.py
│   │   │   └── topic.py
│   │   └── user_models
│   │       ├── __init__.py
│   │       └── user.py
│   ├── services
│   │   ├── auth_service
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py
│   │   ├── azure_function_service
│   │   │   ├── __init__.py
│   │   │   └── azure_function_service.py
│   │   ├── feeds_service
│   │   │   ├── __init__.py
│   │   │   ├── feed_data_handler.py
│   │   │   ├── feeds_service.py
│   │   │   ├── pagination_service.py
│   │   │   ├── resources_service.py
│   │   │   └── topics_service.py
│   │   │
│   │   │────── user_service
│   │   │    ├── __init__.py
│   │   │    ├── user_service.py
│   │   │   
│   │   ├────── base_validation_service.py
│   │
│   ├── __init__.py
│   │── extensions.py
│   ├── database/
│       ├── __init__.py
│       ├── database.py
│       └── startup_seeder.py
│
│
├── instance/
│
│──────── migrations/
│       ├── alembic.ini
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
│           
│
├── tests/
│
├── venv/
│
├── app.py
├── app.log
├── config.py
├── Dockerfile
├── DockerfileProd
├── docker-compose.yml
├── example.env
├── env.py
├── alembic.ini
├── requirements.txt
├── newsfeed.db
├── project_structure.md
├── README.md
└── .gitignore
