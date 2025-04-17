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

#### Current API Routes

**Auth Routes (`/`)** (`api/backend/auth/auth_routes.py`)

- `POST /login`: Register a new user. Requires `name`, `email`, `password`. Optional: `major`, `learning_style`, `availability`. Returns `user_id`.
- `PUT /login`: Log in an existing user. Requires `email`, `password`. Returns `user_id`.
- `GET /login`: Test route to fetch all users.

**User Profile Routes (`/users`)** (`api/backend/user_profile/profile_routes.py`)

- `GET /users/all`: Fetches details for all users (name, email, major, etc.).
- `GET /users/<user_id>`: Gets details for a specific user.
- `PUT /users/<user_id>`: Updates a user's profile. Requires at least one field from: `name`, `email`, `major`, `learning_style`, `availability`.
- `DELETE /users/<user_id>`: Deletes a user account.
- `GET /users/<user_id>/groups`: Fetches all study groups (ID and Name) the given user is a member of.
- `GET /users/<user_id>/potential-matches`: Fetches up to 5 potential study matches, excluding the current user and existing matches.

**User Resource Routes (`/`)** (`api/backend/user_resources/resource_routes.py`)

- `GET /users/<user_id>/resources`: Retrieve all resources associated with a user.
- `POST /users/<user_id>/resources`: Add a new resource for the user. Requires `link`, `type`.
- `PUT /resources/<resource_id>`: Updates an existing resource. Requires `link` and/or `type`.
- `DELETE /resources/<resource_id>`: Deletes a resource and its associations.

**User Matching Routes (`/`)** (`api/backend/user_matching/matching_routes.py`)

- `POST /matches`: Records a new match between two users. Requires `user1_id`, `user2_id`. Returns success or "already exists" message.
- `POST /users/<user_id>/study-partners`: Find study partners for a user in a course. Requires `course_id` in body. Excludes self and existing matches.
- `GET /users/<user_id>/matches`: Fetches the unique names and IDs of users matched with the given user.
- `PUT /matches/<user1_id>/<user2_id>`: Updates details of an existing match (placeholder - requires `status`).
- `DELETE /matches/<user1_id>/<user2_id>`: Deletes a match record.

**User Group Routes (`/groups`)** (`api/backend/user_groups/group_routes.py`)

- `GET /groups/find`: Fetches all available study groups (ID and Name).
- `POST /groups/create`: Creates a new study group and adds creator as member. Requires `group_name`, `user_id`.
- `POST /groups/<group_id>/join`: Adds a user to a specific study group. Requires `user_id` in body. Returns success or already exists message.
- `PUT /groups/<group_id>`: Updates group information. Requires `group_name`.
- `DELETE /groups/<group_id>`: Deletes a study group and removes members.

**Data Analyst Routes (`/a`)** (`api/backend/data_analyst/analyst_routes.py`)

- `GET /a/matches/total`: Gets the total count of matches recorded.
- `GET /a/analytics/retention`: Gets user retention rate (placeholder logic).
