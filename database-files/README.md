# `database-files` Folder

This folder contains files related to the MySQL database used by the StudyBuddy application, specifically for the `mysql_db` Docker container.

## How it Works

- **Initialization Script:** The primary file here is `study_buddy.sql`. This SQL script contains the necessary `CREATE TABLE` statements to define the database schema (structure) and `INSERT` statements to populate the database with initial sample data.
- **Docker Volume Mount:** When the Docker services are started using `docker-compose up`, the MySQL container (`mysql_db`) is configured to look for SQL scripts in a special initialization directory (`/docker-entrypoint-initdb.d/`). The `docker-compose.yml` file mounts the contents of this `database-files` folder into that directory within the container.
- **Automatic Initialization:** If the MySQL container starts and finds that its data volume (where the actual database tables and data are stored) is empty or uninitialized, it will automatically execute any `.sql` files found in the `/docker-entrypoint-initdb.d/` directory. This process creates the schema and inserts the sample data defined in `study_buddy.sql`.
- **Persistence:** Once initialized, the database data persists in a Docker volume associated with the `mysql_db` container. Subsequent container restarts will use the existing data unless the volume is explicitly removed.

## How to Re-Bootstrap (Reset) the Database

If you need to completely reset the database to its initial state (as defined by `study_buddy.sql`), you need to remove the persistent data volume associated with the `mysql_db` container. **Warning: This will permanently delete all current data in the database.**

1.  **Stop Containers:** Make sure all Docker containers for the project are stopped. You can do this from the project's root directory:

    docker-compose down

2.  **Remove Volumes:** Use the `--volumes` flag with the `down` command to remove the named volumes defined in `docker-compose.yml`, including the one used by the database:

    docker-compose down --volumes

3.  **Restart Containers:** Start the containers again. Since the database volume was removed, the `mysql_db` container will re-initialize by running the `study_buddy.sql` script.

    docker-compose up --build

- -- build flag is nessecary if you are rebuildin the container, or if major changes have been made to the database schema and/or if you want recently inserted sample data to appear into the database.

After these steps, the database will be reset to the schema and sample data contained in `study_buddy.sql`.

## Schema Overview

The `study_buddy.sql` script defines the following main tables:

**Core Entities:**

- **`user`**: Stores user profiles including login credentials, name, email, major, learning style, and availability. This is a central table; many others relate back to it. (Participation: Mandatory Base)
- **`admin`**: Stores information about system administrators. (Participation: Mandatory Base)
- **`study_group`**: Represents study groups created by users, identified by an ID and name. (Participation: Mandatory Base)
- **`course`**: Details about courses offered, including name and department. Linked to `university`. (Participation: Mandatory Base)
- **`resource`**: Contains information about shared study resources, like links and types. (Participation: Mandatory Base)
- **`interests`**: A lookup table for predefined academic or study interests. (Participation: Mandatory Base)
- **`university`**: A lookup table for university names. (Participation: Mandatory Base)

**Junction Tables (Many-to-Many Relationships):**

- **`group_student`**: Links `user` (as `studentid`) to `study_group`, representing group membership. A user can be in multiple groups, and a group can have multiple students. (Participation: Junction - Optional for `user` and `study_group`)
- **`matched_with`**: Links two `user` records (`user1_id`, `user2_id`) to represent a confirmed study partner match. A user can have multiple matches. (Participation: Junction - Optional for `user`)
- **`user_resource`**: Links `user` to `resource`, allowing users to save or associate with multiple resources, and resources to be used by multiple users. (Participation: Junction - Optional for `user` and `resource`)
- **`user_interests`**: Links `user` to `interests`, allowing users to specify multiple areas of interest. (Participation: Junction - Optional for `user` and `interests`)
- **`enrollment`** (Assumed/Typical): Would link `user` and `course`. A user can enroll in multiple courses, and a course can have multiple users. (Participation: Junction - Optional for `user` and `course` - _Note: Table definition might be missing or implicit_).

**Supporting/Optional Tables:**

- **`compatibility`**: Stores detailed compatibility preferences for a `user` (1-to-1). A user may or may not have these defined. (Participation: Optional Extension of `user`)
- **`study_session`**: Records instances of study sessions, linked to a `course` and a `user` (presumably the one initiating or involved). (Participation: Optional Activity Log)
- **`matchhistory`**: Appears to store historical match scores related to a `user`. (Participation: Optional Log)
- **`systemlog`**: Logs actions performed by `admin` users. (Participation: Optional Log)
- **`serverstatus`**: Stores server performance metrics. (Participation: Optional System Info)
- **`effectiveness`**: Stores general feedback or metrics about the platform's effectiveness. (Participation: Optional System Info)

**Participation Notes:**

- **Mandatory Base:** These tables represent core concepts (like Users, Groups, Courses) that are expected to exist.
- **Junction:** These tables exist solely to connect two other tables in a many-to-many relationship. An entry in a junction table is optional from the perspective of the core tables it links (e.g., a User doesn't _have_ to be in a Group).
- **Optional:** These tables add extra information or track activities/logs but are not strictly required for the core functionality concerning a specific User, Group, etc. (e.g., a User doesn't _need_ to have compatibility info defined).
