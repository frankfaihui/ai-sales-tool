# AI Sales Tool Demo

Welcome to ai sales tool Project! This repository showcases an OpenAI API, a flask application, a next.js app, MongoDB, and uses Docker Compose for easy setup.

A working demo can be found at [http://ai-sales-tool.devfaihui.link/](http://ai-sales-tool.devfaihui.link/)

## Overview

### Sub-Projects

The project is organized into the following sub-projects:

1. **ai-sales-api (Flask App)**

   The ai-sales-api project is a Flask application responsible for handling API requests and interactions with the OpenAI API.
2. **ai-sales-web (Next.js App)**

   The ai-sales-web project is a Next.js application responsible for the web interface and user interactions.

### Database

The project uses MongoDB as its database. The database is automatically set up and configured when running the main application with Docker Compose.

MongoDB connection information:

- **Host**: `localhost`
- **Port**: `27017`

## Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

### Running with Docker Compose

1. **Clone the repository:**

   ```bash
   git clone https://github.com/frankfaihui/ai-sales-tool
   ```

2. **Navigate to the project directory:**

    ```bash
    cd ai-sales-tool
    ```

3. **Create a `.env` file:**

    ```bash
    cp .env.example .env
    ```

    Update the `.env` file with your OpenAI API key.

4. **Start the application:**

    ```bash
    docker-compose up
    ```

    The application will be available at `http://localhost:3000`.
