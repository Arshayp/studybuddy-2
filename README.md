# StudyBuddy CS3200 Final Project README

## breakdown:

- api/ => handles the backend Flask API (web-api container)
- app/ => streamlit frontend (all files are in src/pages. Our project files do not start with a number that the template ones did)
- database-files => myssql_db container. the only relevant file is study_buddy.sql, which contains the schema and sample data.

## how to set up:

- in the api/ folder, copy all the contents of the .env.template file and paste it into a new file WITHIN the api/ folder called '.env'.

- save all files
- docker-compose down --volumes

  - only if there is an old version of the container in docker

- docker-compose up --build
  - check docker if one of the containers is not running, this is likely because there is some error in the files.

## running instructions:

- frontend on http://localhost:8501
- backend on http://localhost:4000

## what we did :

### Frontend

- user- facing side:
  - user dashboard (dashboard.py)
  - user login (login.py)
  - user registration (register.py)
  - study groups finding, joining, management and creation (study_groups.py)
  - finding individual study partners (matching.py)

### backend:

- user-facing features.
  - made routes for auth in the auth/ folder.

#### Auth Routes (`api/backend/auth/auth_routes.py`) => auth blueprint (no prefix)

- `POST /login`: Register a new user. Requires `name`, `email`, `password`. Optional: `major`, `learning_style`, `availability`.
- `PUT /login`: Log in an existing user. Requires `email`, `password`. Returns `user_id`.
- `GET /login`: Test route to fetch all users.

#### User Routes (`api/backend/users/user_routes.py`) => user blueprint (all routes below are preceeded with '/u)

- `GET /all`: Test route to fetch all users.
- `GET /<user_id>/study-partners`: Find partners for a user in a course (requires `course_id` query param).
- `GET /<user_id>/resources`: Get resources for a user.
- `POST /<user_id>/resources`: Add a resource for a user (requires `link`, `type`).
- `POST /potential-matches`: Get potential study matches for a user (requires `user_id`).
- `POST /groups/all`: Get groups a user is in (requires `user_id`).
- `GET /groups/find`: Get all available study groups.
- `POST /groups/create`: Create a study group (requires `group_name`, `description`).
- `POST /groups/join`: Add a user to a group (requires `user_id`, `group_id`).
- `POST /match/success`: Record a successful match (requires `user_id1`, `user_id2`).
- `GET /match/<user_id>/matches`: Get successful matches for a user.

#### Data Analyst Routes (`api/backend/data_analyst/analyst_routes.py`)
