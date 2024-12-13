# API Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Namespaces Overview](#namespaces-overview)
   - [Users Namespace (`/users`)](#users-namespace-users)
   - [Speech-to-Text Namespace (`/stt`)](#speech-to-text-namespace-stt)
   - [Named Entity Recognition Namespace (`/ner`)](#named-entity-recognition-namespace-ner)
   - [Pathfinding Namespace (`/pathfinding`)](#pathfinding-namespace-pathfinding)
   - [General Processes Namespace (`/general`)](#general-processes-namespace-general)
3. [Static Files Endpoints](#static-files-endpoints)
4. [Data Models](#data-models)
   - [User Model](#user-model)
   - [NER Input Model](#ner-input-model)
   - [Pathfinding Input Model](#pathfinding-input-model)
   - [General Process Input Model](#general-process-input-model)
5. [Error Handling](#error-handling)
6. [Database Migrations](#database-migrations)
7. [Example Requests and Responses](#example-requests-and-responses)
   - [Users Endpoints](#users-endpoints)
   - [STT Endpoint](#stt-endpoint)
   - [NER Endpoint](#ner-endpoint)
   - [Pathfinding Endpoint](#pathfinding-endpoint)
   - [General Process Endpoint](#general-process-endpoint)
8. [Implementation Details](#implementation-details)
9. [Running initialization Vosk](#vosk-init)
10. [Conclusion](#conclusion)
    
[known issues](#known-issues)
## Introduction

This API serves as a comprehensive backend solution integrating multiple services such as User Management, Speech-to-Text (STT), Named Entity Recognition (NER), and Pathfinding. Additionally, it offers a general processing route that combines NER and Pathfinding to provide seamless functionality from text input to route optimization.

The API is built using **Flask** and **Flask-RESTx**, facilitating organized namespaces and structured endpoints. Below is a detailed overview of each namespace, their respective endpoints, data models, migration steps, and usage examples.

## Namespaces Overview

The API is divided into several namespaces, each responsible for distinct functionalities:

1. **Users Namespace (`/users`)**: Handles user-related operations such as creating, retrieving, updating, and deleting users.
2. **Speech-to-Text Namespace (`/stt`)**: Manages audio file processing to convert speech into text.
3. **Named Entity Recognition Namespace (`/ner`)**: Extracts entities (e.g., locations) from text inputs.
4. **Pathfinding Namespace (`/pathfinding`)**: Computes optimal paths between specified stations using various algorithms.
5. **General Processes Namespace (`/general`)**: Integrates NER and Pathfinding services to process text inputs and provide pathfinding results.

### Users Namespace (`/users`)

**Base URL**: `/users`

**Description**: Manages user data, including creation, retrieval, updating, and deletion of user records.

#### Endpoints

1. **List All Users**
   - **URL**: `/users/`
   - **Method**: `GET`
   - **Description**: Retrieves a list of all users.
   - **Response**: JSON array of user objects.

2. **Create a New User**
   - **URL**: `/users/`
   - **Method**: `POST`
   - **Description**: Creates a new user with provided name and email.
   - **Request Body**:
     ```json
     {
       "name": "John Doe",
       "email": "john.doe@example.com"
     }
     ```
   - **Response**: JSON object of the created user with status code `201 Created`.

3. **Get User by ID**
   - **URL**: `/users/{id}`
   - **Method**: `GET`
   - **Description**: Retrieves a user by their unique identifier.
   - **Response**: JSON object of the user.

4. **Update User by ID**
   - **URL**: `/users/{id}`
   - **Method**: `PUT`
   - **Description**: Updates the name and/or email of an existing user.
   - **Request Body**:
     ```json
     {
       "name": "Jane Doe",
       "email": "jane.doe@example.com"
     }
     ```
   - **Response**: JSON object of the updated user.

5. **Delete User by ID**
   - **URL**: `/users/{id}`
   - **Method**: `DELETE`
   - **Description**: Deletes a user by their unique identifier.
   - **Response**: Empty response with status code `204 No Content`.

### Speech-to-Text Namespace (`/stt`)

**Base URL**: `/stt`

**Description**: Handles processing of audio files to convert speech into text.

#### Endpoints

1. **Process Audio File**
   - **URL**: `/stt/`
   - **Method**: `POST`
   - **Description**: Accepts an audio file and returns the transcribed text.
   - **Request**:
     - **Content-Type**: `multipart/form-data`
     - **Form Data**:
       - `file`: Audio file in WAV format.
   - **Response**:
     ```json
     {
       "transcript": "Your transcribed text here."
     }
     ```
   - **Allowed File Types**: `.wav`
   - **Error Responses**:
     - `400 Bad Request`: If no file is provided or the file type is not allowed.

### Named Entity Recognition Namespace (`/ner`)

**Base URL**: `/ner`

**Description**: Extracts entities such as locations from text inputs.

#### Endpoints

1. **Extract Entities**
   - **URL**: `/ner/`
   - **Method**: `POST`
   - **Description**: Processes text input to extract named entities.
   - **Request Body**:
     ```json
     {
       "text": "Find the best route from Paris to Lyon."
     }
     ```
   - **Response**:
     ```json
     {
       "entities": [
         {"status": "start", "station": "Paris"},
         {"status": "end", "station": "Lyon"}
       ]
     }
     ```
   - **Error Responses**:
     - `400 Bad Request`: If no text is provided or if NER processing fails.

### Pathfinding Namespace (`/pathfinding`)

**Base URL**: `/pathfinding`

**Description**: Computes optimal paths between specified stations using various algorithms.

#### Endpoints

1. **Find Path**
   - **URL**: `/pathfinding/`
   - **Method**: `POST`
   - **Description**: Finds the optimal path between two stations using the specified algorithm.
   - **Request Body**:
     ```json
     {
       "start": "Paris",
       "end": "Lyon",
       "algorithm": "AStar"
     }
     ```
     - **Parameters**:
       - `start` (string, required): Name of the start station.
       - `end` (string, required): Name of the end station.
       - `algorithm` (string, optional): Pathfinding algorithm to use. Defaults to `AStar`. Options include:
         - `AStar`
         - `Dijkstra`
         - `BFS`
         - `DFS`
         - `BellmanFord`
         - `UCS`
         - `BidirectionalAStar`
   - **Response**:
     ```json
     {
       "path": ["Paris", "Intermediate Station", "Lyon"],
       "distance": 300.5,
       "tries": 25,
       "time": 0.123,
       "path_length": 3,
       "memory_usage": 0.001234,
       "explored_nodes": 25,
       "average_node_time": 0.00492,
       "map_url": "/static/maps/map_uniqueid.html"
     }
     ```
   - **Error Responses**:
     - `400 Bad Request`: If required parameters are missing or if pathfinding fails.

### General Processes Namespace (`/general`)

**Base URL**: `/general`

**Description**: Integrates NER and Pathfinding services to process text inputs and provide optimized paths based on extracted entities.

#### Endpoints

1. **Process Text to Find Path**
   - **URL**: `/general/process`
   - **Method**: `POST`
   - **Description**: Takes text input, extracts start and end stations using NER, and finds the optimal path between them.
   - **Request Body**:
     ```json
     {
       "text": "Find the best route from La Douzillère to Chalonnes."
     }
     ```
   - **Response**:
     ```json
     {
       "entities": [
         {"status": "start", "station": "La Douzillère"},
         {"status": "end", "station": "Chalonnes"}
       ],
       "pathfinding_result": {
         "path": ["La Douzillère", "Intermediate Station", "Chalonnes"],
         "distance": 120.5,
         "tries": 30,
         "time": 0.456,
         "path_length": 3,
         "memory_usage": 0.001234,
         "explored_nodes": 30,
         "average_node_time": 0.0152,
         "map_url": "/static/maps/map_uniqueid.html"
       }
     }
     ```
   - **Processing Flow**:
     1. **NER Extraction**: Extracts `start` and `end` stations from the provided text using NER.
     2. **Pathfinding**: Uses the extracted station names to compute the optimal path with the default algorithm `AStar`.
   - **Error Responses**:
     - `400 Bad Request`: If text input is missing, if NER fails to extract required entities, or if pathfinding fails.

## Static Files Endpoints

The API provides endpoints to serve static files such as client-side HTML, JavaScript, and generated map files.

### Endpoints

1. **Serve Static Files**
   - **URL**: `/static/<path:filename>`
   - **Method**: `GET`
   - **Description**: Serves static files located in the `static` directory.
   - **Parameters**:
     - `filename` (path): The path to the static file within the `static` directory.
   - **Response**: Returns the requested static file.

2. **Serve Map Files**
   - **URL**: `/static/maps/<path:filename>`
   - **Method**: `GET`
   - **Description**: Serves map files generated by the Pathfinding service.
   - **Parameters**:
     - `filename` (path): The name of the map file within the `static/maps` directory.
   - **Response**: Returns the requested map HTML file.

## Data Models

The API utilizes various data models to structure request and response data.

### User Model

**Namespace**: `/users`

**Definition**:
```python
user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
})
```

### NER Input Model

**Namespace**: `/ner`

**Definition**:
```python
ner_model = ner_ns.model('TextInput', {
    'text': fields.String(required=True, description='Text input')
})
```

### Pathfinding Input Model

**Namespace**: `/pathfinding`

**Definition**:
```python
path_model = path_ns.model('PathInput', {
    'start': fields.String(required=True, description='Start station code'),
    'end': fields.String(required=True, description='End station code'),
    'algorithm': fields.String(
        required=False,
        description='Algorithm to use',
        enum=['AStar', 'Dijkstra', 'BFS', 'DFS', 'BellmanFord', 'UCS', 'BidirectionalAStar'],
        default='AStar')
})
```

### General Process Input Model

**Namespace**: `/general`

**Definition**:
```python
general_process_model = general_processes_ns.model('GeneralProcessInput', {
    'text': fields.String(required=True, description='Text input to process')
})
```

## Error Handling

The API consistently uses HTTP status codes to indicate the success or failure of an API request. Errors are returned with appropriate HTTP status codes and descriptive messages.

- **400 Bad Request**: Indicates issues with the request data, such as missing fields or invalid data formats.
  - **Response Structure**:
    ```json
    {
      "message": "Error description here."
    }
    ```
- **404 Not Found**: Indicates that a requested resource (e.g., user) does not exist.
  - **Response Structure**:
    ```json
    {
      "message": "User not found."
    }
    ```
- **500 Internal Server Error**: Indicates unexpected server-side errors.
  - **Response Structure**:
    ```json
    {
      "message": "Internal server error."
    }
    ```

**Example Error Responses**:

1. **Missing Required Field**:
   - **Status**: `400 Bad Request`
   - **Response**:
     ```json
     {
       "message": "Start and end station names are required"
     }
     ```

2. **Resource Not Found**:
   - **Status**: `404 Not Found`
   - **Response**:
     ```json
     {
       "message": "User not found."
     }
     ```

3. **Processing Error**:
   - **Status**: `400 Bad Request`
   - **Response**:
     ```json
     {
       "message": "NER Error: Unable to extract entities."
     }
     ```


## Database Migrations

The API utilizes **Flask-Migrate** for handling database migrations. This allows for version control of the database schema and seamless updates as the application evolves.

### Setting Up Migrations

Follow these steps to initialize and manage database migrations:

1. **Set the Flask App Environment Variable**
   - This tells Flask which application to use for running commands.
   - **Command**:
     ```bash
     export FLASK_APP=manage.py
     ```

2. **Initialize the Migration Repository**
   - Sets up the migrations directory.
   - **Command**:
     ```bash
     flask db init
     ```

3. **Create an Initial Migration**
   - Generates a migration script based on the current database models.
   - **Command**:
     ```bash
     flask db migrate -m "Initial migration."
     ```

4. **Apply the Migration to the Database**
   - Updates the database schema to match the models.
   - **Command**:
     ```bash
     flask db upgrade
     ```

### Migration Commands Overview

- `flask db init`: Initializes a new migration repository. Run this command once at the start of your project.
- `flask db migrate -m "Message"`: Generates a new migration script. The `-m` flag allows you to add a message describing the migration.
- `flask db upgrade`: Applies the migration scripts to the database, updating the schema to the latest version.
- `flask db downgrade`: Reverts the database schema to a previous migration state.
- `flask db history`: Shows the history of migrations.
- `flask db current`: Displays the current migration applied to the database.
- `flask db show <revision>`: Shows the details of a specific migration revision.

### Important Notes

- **Version Control**: Ensure that your migration scripts are version-controlled (e.g., using Git) to track changes over time.
- **Testing Migrations**: Always test migrations in a development or staging environment before applying them to production.
- **Handling Conflicts**: In team environments, coordinate migrations to prevent conflicts and ensure consistent database states.

## Example Requests and Responses

### Users Endpoints

#### 1. List All Users

- **Request**:
  - **Method**: `GET`
  - **URL**: `/users/`

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      }
    ]
    ```

#### 2. Create a New User

- **Request**:
  - **Method**: `POST`
  - **URL**: `/users/`
  - **Body**:
    ```json
    {
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com"
    }
    ```

- **Response**:
  - **Status**: `201 Created`
  - **Body**:
    ```json
    {
      "id": 3,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com"
    }
    ```

#### 3. Get User by ID

- **Request**:
  - **Method**: `GET`
  - **URL**: `/users/1`

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
    ```

#### 4. Update User by ID

- **Request**:
  - **Method**: `PUT`
  - **URL**: `/users/1`
  - **Body**:
    ```json
    {
      "name": "Johnathan Doe",
      "email": "johnathan.doe@example.com"
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "id": 1,
      "name": "Johnathan Doe",
      "email": "johnathan.doe@example.com"
    }
    ```

#### 5. Delete User by ID

- **Request**:
  - **Method**: `DELETE`
  - **URL**: `/users/1`

- **Response**:
  - **Status**: `204 No Content`
  - **Body**: *Empty*

### STT Endpoint

#### Process Audio File

- **Request**:
  - **Method**: `POST`
  - **URL**: `/stt/`
  - **Headers**: `Content-Type: multipart/form-data`
  - **Body**: Form-data with a file field named `file` containing a `.wav` audio file.

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "transcript": "Find the best route from Paris to Lyon."
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "No audio file provided or file type not allowed."
    }
    ```

### NER Endpoint

#### Extract Entities

- **Request**:
  - **Method**: `POST`
  - **URL**: `/ner/`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "text": "Find the best route from Paris to Lyon."
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "entities": [
        {"status": "start", "station": "Paris"},
        {"status": "end", "station": "Lyon"}
      ]
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "No text provided"
    }
    ```

### Pathfinding Endpoint

#### Find Path

- **Request**:
  - **Method**: `POST`
  - **URL**: `/pathfinding/`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "start": "Paris",
      "end": "Lyon",
      "algorithm": "AStar"
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "path": ["Paris", "Intermediate Station", "Lyon"],
      "distance": 300.5,
      "tries": 25,
      "time": 0.123,
      "path_length": 3,
      "memory_usage": 0.001234,
      "explored_nodes": 25,
      "average_node_time": 0.00492,
      "map_url": "/static/maps/map_uniqueid.html"
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "Start and end station names are required"
    }
    ```

### General Process Endpoint

#### Process Text to Find Path

- **Request**:
  - **Method**: `POST`
  - **URL**: `/general/process`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "text": "Find the best route from La Douzillère to Chalonnes."
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "entities": [
        {"status": "start", "station": "La Douzillère"},
        {"status": "end", "station": "Chalonnes"}
      ],
      "pathfinding_result": {
        "path": ["La Douzillère", "Intermediate Station", "Chalonnes"],
        "distance": 120.5,
        "tries": 30,
        "time": 0.456,
        "path_length": 3,
        "memory_usage": 0.001234,
        "explored_nodes": 30,
        "average_node_time": 0.0152,
        "map_url": "/static/maps/map_uniqueid.html"
      }
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "Unable to extract start and end stations from text"
    }
    ```

## Database Migrations

The API utilizes **Flask-Migrate** for handling database migrations. This allows for version control of the database schema and seamless updates as the application evolves.

### Setting Up Migrations

Follow these steps to initialize and manage database migrations:

1. **Set the Flask App Environment Variable**
   - This tells Flask which application to use for running commands.
   - **Command**:
     ```bash
     export FLASK_APP=manage.py
     ```

2. **Initialize the Migration Repository**
   - Sets up the migrations directory.
   - **Command**:
     ```bash
     flask db init
     ```

3. **Create an Initial Migration**
   - Generates a migration script based on the current database models.
   - **Command**:
     ```bash
     flask db migrate -m "Initial migration."
     ```

4. **Apply the Migration to the Database**
   - Updates the database schema to match the models.
   - **Command**:
     ```bash
     flask db upgrade
     ```

### Migration Commands Overview

- `flask db init`: Initializes a new migration repository. Run this command once at the start of your project.
- `flask db migrate -m "Message"`: Generates a new migration script. The `-m` flag allows you to add a message describing the migration.
- `flask db upgrade`: Applies the migration scripts to the database, updating the schema to the latest version.
- `flask db downgrade`: Reverts the database schema to a previous migration state.
- `flask db history`: Shows the history of migrations.
- `flask db current`: Displays the current migration applied to the database.
- `flask db show <revision>`: Shows the details of a specific migration revision.

### Important Notes

- **Version Control**: Ensure that your migration scripts are version-controlled (e.g., using Git) to track changes over time.
- **Testing Migrations**: Always test migrations in a development or staging environment before applying them to production.
- **Handling Conflicts**: In team environments, coordinate migrations to prevent conflicts and ensure consistent database states.

## Example Requests and Responses

### Users Endpoints

#### 1. List All Users

- **Request**:
  - **Method**: `GET`
  - **URL**: `/users/`

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
      }
    ]
    ```

#### 2. Create a New User

- **Request**:
  - **Method**: `POST`
  - **URL**: `/users/`
  - **Body**:
    ```json
    {
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com"
    }
    ```

- **Response**:
  - **Status**: `201 Created`
  - **Body**:
    ```json
    {
      "id": 3,
      "name": "Alice Johnson",
      "email": "alice.johnson@example.com"
    }
    ```

#### 3. Get User by ID

- **Request**:
  - **Method**: `GET`
  - **URL**: `/users/1`

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
    ```

### STT Endpoint

#### Process Audio File

- **Request**:
  - **Method**: `POST`
  - **URL**: `/stt/`
  - **Headers**: `Content-Type: multipart/form-data`
  - **Body**: Form-data with a file field named `file` containing a `.wav` audio file.

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "transcript": "Find the best route from Paris to Lyon."
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "No audio file provided or file type not allowed."
    }
    ```

### NER Endpoint

#### Extract Entities

- **Request**:
  - **Method**: `POST`
  - **URL**: `/ner/`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "text": "Find the best route from Paris to Lyon."
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "entities": [
        {"status": "start", "station": "Paris"},
        {"status": "end", "station": "Lyon"}
      ]
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "No text provided"
    }
    ```

### Pathfinding Endpoint

#### Find Path

- **Request**:
  - **Method**: `POST`
  - **URL**: `/pathfinding/`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "start": "Paris",
      "end": "Lyon",
      "algorithm": "AStar"
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "path": ["Paris", "Intermediate Station", "Lyon"],
      "distance": 300.5,
      "tries": 25,
      "time": 0.123,
      "path_length": 3,
      "memory_usage": 0.001234,
      "explored_nodes": 25,
      "average_node_time": 0.00492,
      "map_url": "/static/maps/map_uniqueid.html"
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "Start and end station names are required"
    }
    ```

### General Process Endpoint

#### Process Text to Find Path

- **Request**:
  - **Method**: `POST`
  - **URL**: `/general/process`
  - **Headers**: `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "text": "Find the best route from La Douzillère to Chalonnes."
    }
    ```

- **Response**:
  - **Status**: `200 OK`
  - **Body**:
    ```json
    {
      "entities": [
        {"status": "start", "station": "La Douzillère"},
        {"status": "end", "station": "Chalonnes"}
      ],
      "pathfinding_result": {
        "path": ["La Douzillère", "Intermediate Station", "Chalonnes"],
        "distance": 120.5,
        "tries": 30,
        "time": 0.456,
        "path_length": 3,
        "memory_usage": 0.001234,
        "explored_nodes": 30,
        "average_node_time": 0.0152,
        "map_url": "/static/maps/map_uniqueid.html"
      }
    }
    ```

- **Error Response**:
  - **Status**: `400 Bad Request`
  - **Body**:
    ```json
    {
      "message": "Unable to extract start and end stations from text"
    }
    ```

## Database Migrations

The API utilizes **Flask-Migrate** for handling database migrations. This allows for version control of the database schema and seamless updates as the application evolves.

### Setting Up Migrations

Follow these steps to initialize and manage database migrations:

1. **Set the Flask App Environment Variable**
   - This tells Flask which application to use for running commands.
   - **Command**:
     ```bash
     export FLASK_APP=manage.py
     ```

2. **Initialize the Migration Repository**
   - Sets up the migrations directory.
   - **Command**:
     ```bash
     flask db init
     ```

3. **Create an Initial Migration**
   - Generates a migration script based on the current database models.
   - **Command**:
     ```bash
     flask db migrate -m "Initial migration."
     ```

4. **Apply the Migration to the Database**
   - Updates the database schema to match the models.
   - **Command**:
     ```bash
     flask db upgrade
     ```

### Migration Commands Overview

- `flask db init`: Initializes a new migration repository. Run this command once at the start of your project.
- `flask db migrate -m "Message"`: Generates a new migration script. The `-m` flag allows you to add a message describing the migration.
- `flask db upgrade`: Applies the migration scripts to the database, updating the schema to the latest version.
- `flask db downgrade`: Reverts the database schema to a previous migration state.
- `flask db history`: Shows the history of migrations.
- `flask db current`: Displays the current migration applied to the database.
- `flask db show <revision>`: Shows the details of a specific migration revision.

### Important Notes

- **Version Control**: Ensure that your migration scripts are version-controlled (e.g., using Git) to track changes over time.
- **Testing Migrations**: Always test migrations in a development or staging environment before applying them to production.
- **Handling Conflicts**: In team environments, coordinate migrations to prevent conflicts and ensure consistent database states.

## Implementation Details

### Namespace Registration

The `register_routes` function is responsible for adding all defined namespaces to the Flask-RESTx API instance. This ensures that each namespace and its associated routes are properly integrated into the API.

```python
def register_routes(api):
    # Add Namespaces to API
    api.add_namespace(user_ns)
    api.add_namespace(stt_ns)
    api.add_namespace(ner_ns)
    api.add_namespace(path_ns)
    api.add_namespace(general_processes_ns)
    
    # ... [Endpoint Definitions] ...
```
    
### User Management

- **CRUD Operations**: The Users namespace provides standard Create, Read, Update, and Delete (CRUD) operations for managing user data.
- **Database Interaction**: Utilizes SQLAlchemy models (`User`) and schemas (`UserSchema`) for database operations and serialization/deserialization of user data.
    
### Speech-to-Text (STT) Processing

- **File Upload**: Accepts `.wav` audio files via multipart/form-data.
- **Transcript Generation**: Processes the uploaded audio file using the `stt_service.process_audio_file` method to generate a text transcript.
    
### Named Entity Recognition (NER)
    
- **Text Input**: Accepts raw text input in JSON format.
- **Entity Extraction**: Utilizes the `ner_service.extract_entities` method to identify and extract entities from the provided text.
- **Output Format**: Returns a list of entities with their status (`start` or `end`) and corresponding station names.
    
### Pathfinding
    
- **Input Parameters**: Requires `start` and `end` station names, with an optional `algorithm` parameter to specify the pathfinding algorithm.
- **Path Computation**: Leverages the `pathfinding_service.find_path` method to compute the optimal path based on the provided parameters.
- **Response Data**: Includes detailed information about the path, such as distance, computation time, memory usage, and a URL to the generated map.
    
### General Processes
    
- **Integrated Flow**: Combines NER and Pathfinding services to process text inputs and provide optimized paths based on extracted entities.
- **Processing Steps**:
  1. **Entity Extraction**: Extracts `start` and `end` stations from the provided text using NER.
  2. **Pathfinding**: Uses the extracted station names to compute the optimal path with the default algorithm `AStar`.
- **Response Structure**: Returns both the extracted entities and the pathfinding results, including a map URL.
    
### Static Files Serving
    
- **Static Files**: The API provides endpoints to serve static files located in the `static` directory.
  - **General Static Files**: Accessible via `/static/{filename}`.
  - **Map Files**: Accessible via `/static/maps/{filename}`.
- **Usage**: Primarily used to serve client-side assets and dynamically generated map files resulting from pathfinding operations.
    
## Initialize Vosk
  You can either download vosk manually and place it inside the app/models folder (unzipped) such as that 
  it should be API/app/models/vosk-model... or you can run the bash command setup_vosk.sh by running
  ./setup_vosk.sh only on linux and darwin (macOS) systems

## Conclusion

This API offers a robust and organized backend solution integrating multiple services to provide comprehensive functionalities ranging from user management to advanced text processing and pathfinding. By organizing endpoints into dedicated namespaces and employing consistent data models and error handling practices, the API ensures scalability, maintainability, and ease of use for both developers and clients.

**Key Features**:

- **Modular Design**: Organized into distinct namespaces for clarity and maintainability.
- **Comprehensive Functionality**: From managing users to processing complex text inputs for optimized routing.
- **Error Handling**: Consistent and informative error responses to aid in debugging and user feedback.
- **Static File Serving**: Efficiently serves both general and map-specific static files.
- **Database Migrations**: Manages database schema changes using Flask-Migrate for smooth evolution of the database structure.

**Next Steps**:

- **Authentication & Authorization**: Implement security measures to protect user data and restrict access to certain endpoints.
- **Enhanced Validation**: Incorporate more rigorous input validation to ensure data integrity.
- **Scalability Considerations**: Optimize services for handling larger datasets and higher traffic volumes.
- **Documentation Integration**: Utilize Swagger UI or similar tools for interactive API documentation, enhancing developer experience.
- **Automated Testing**: Develop tests to ensure the reliability and correctness of the API endpoints.

Feel free to reach out for further assistance or if you need additional features and customizations!

## known issues
- ffmpeg error : if you encounter an error with ffmpeg, you can install it by running the following command
  ```bash
  sudo apt-get install ffmpeg
  ```
  if you are on windows, you can download ffmpeg from the official website and add it to your PATH

- if you encounter an error with the vosk model, you can download it manually from the official website and place it in the app/models folder

- Flask-restx error : if you encounter an error with flask-restx, you can install it by running the following command
  ```bash
  pip install --upgrade flask-restx
  ```

  