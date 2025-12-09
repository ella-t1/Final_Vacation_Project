# Final Vacation Project

This is a comprehensive full-stack web application designed for managing and tracking vacation plans. It consists of two main parts: a user-facing vacation booking website and an administrator statistics dashboard.

## Project Structure

The project is organized into two main sub-projects:

1.  **Vacations Website (`website_vacations`)**:
    *   **Frontend**: React + TypeScript + Vite
    *   **Backend**: Python Flask REST API
    *   **Purpose**: Allows users to view, follow, and manage their vacation plans.

2.  **Statistics Website (`stats_website`)**:
    *   **Frontend**: React + TypeScript + Vite
    *   **Backend**: Python Flask REST API
    *   **Purpose**: A dashboard for administrators to view analytics and statistics about vacation trends and user engagement.

Both applications share a common **PostgreSQL** database.

## Prerequisites

*   **Docker Desktop** installed and running.

## How to Run

The entire project is containerized using Docker and can be started with a single command.

1.  Navigate to the project root directory:
    ```bash
    cd Final_Vacation_Project
    ```

2.  Build and start the services:
    ```bash
    docker-compose up -d
    ```

3.  Access the applications:
    *   **Vacations Website**: [http://localhost:3000](http://localhost:3000)
    *   **Statistics Website**: [http://localhost:3001](http://localhost:3001)

## Development

*   **Database**: The PostgreSQL database runs on port `5432`.
*   **Vacations API**: Running on port `5000`.
*   **Statistics API**: Running on port `5001`.

## Technologies Used

*   **Frontend**: React, TypeScript, Redux Toolkit, SCSS, Vite, Axios
*   **Backend**: Python, Flask, Psycopg2 (Database Driver)
*   **Database**: PostgreSQL
*   **Containerization**: Docker, Docker Compose

## Author

Created as a final project for the full-stack bootcamp.

