# agroforestry_app
# Agroforestry Program Web Application

This web application is designed to manage data for an agroforestry program, allowing field executives, managers, and senior managers to handle and view various details related to farmers, tree species, and field data.

## Features

- User authentication with JWT for secure login.
- Role-based access:
  - **Field Executive**: Can add data related to farmers and tree species.
  - **Field Manager**: Can view data specific to the field executive's inputs.
  - **Senior Manager**: Can view all data and has options to add or delete entries.
- Dashboard that displays data based on the user's role.
- Image handling for field photos uploaded by field executives.
- Secure logout mechanism.

## Prerequisites

Make sure you have the following installed on your local machine:

- Python (3.8 or above)
- MySQL
- pip (Python package manager)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/agroforestry-app.git
    cd agroforestry-app
    ```

2. **Create a virtual environment (optional, but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    Ensure that you have MySQL running and create a database for the app. You can do this with the following commands:

    ```sql
    CREATE DATABASE agroforestry_db;
    ```

    Update your `config.py` file with the correct database credentials (username, password, host, and database name).

5. **Set up the database schema:**

    Run the necessary SQL commands to set up the required tables (you can find these SQL statements in the project folder or implement them based on the app's structure).

    Example:
    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('field_executive', 'field_manager', 'senior_manager') NOT NULL
    );

    CREATE TABLE farmers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        contact_number VARCHAR(255),
        plot_location TEXT,
        field_photo_blob LONGBLOB,
        added_by VARCHAR(255)
    );

    CREATE TABLE tree_species (
        id INT AUTO_INCREMENT PRIMARY KEY,
        farmer_id INT,
        species_name VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        FOREIGN KEY (farmer_id) REFERENCES farmers(id)
    );
    ```

6. **Configure the app (optional):**

    - Update the `SECRET_KEY` and `DB_CONFIG` in the `config.py` file.
    - Ensure that the image files for the logo are placed in the `static/images` folder.

7. **Run the application:**

    Start the Flask server:

    ```bash
    python app.py
    ```

    The app will be available at `http://127.0.0.1:5000/` by default.

## Usage

- **Login**: Navigate to `/login` to log in as a user. Use the credentials for a **field executive**, **field manager**, or **senior manager** based on your role.
- **Dashboard**: Access the dashboard at `/dashboard` to view or manage data based on your role:
  - **Field Executives**: Can submit data via the form.
  - **Field Managers**: View data for specific field executives.
  - **Senior Managers**: View all data and can add or delete records.
- **Logout**: Click on the "Logout" button to log out of the app.

## Testing

Test the app by logging in with different roles and ensure the following:

1. Field executives should be able to submit data and view their entries.
2. Field managers (Manager D) should see only the data for the field executives under them.
3. Senior managers (Manager E) should be able to view all data and have the ability to add or delete records.

## Dependencies

- **Flask**: The web framework.
- **PyJWT**: For handling JSON Web Tokens (JWT).
- **MySQL Connector**: To interact with the MySQL database.
- **Werkzeug**: For file handling (e.g., uploading photos).
- **Datetime**: For token expiration management.

You can install the dependencies with:

```bash
pip install flask pyjwt mysql-connector-python werkzeug
