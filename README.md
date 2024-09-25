# FastAPI & PostgreSQL Backend Template

This repository provides a robust template for building backend applications using
FastAPI and PostgreSQL. It serves as a starting point for creating scalable
and efficient web services with Python.

<details open>
    <summary><h2>Features</h2></summary>

- [**FastAPI**](template_project/api/factories.py#L30): High-performance, asynchronous web framework for building APIs.

- [**Database Session Management**](template_project/db/factories.py#L39): Sessions are
managed using FastAPI's dependency injection system, ensuring proper lifecycle
management that commits on success and rolls back in case of errors.

    ```python
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/")
    async def example(session: Session = Depends(get_session_by_user)):
        pass
    ```

- [**Caching**](template_project/api/cache.py): Configurable caching, supporting both in-memory and Redis-based backends
for better performance and scalability.

    ```python
    from fastapi_cache.decorator import cache

    @cache(namespace="example")
    async def example():
        pass
    ```

- [**SQLModel**](template_project/models/database.py): Combining SQLAlchemy and Pydantic,
SQLModel provides fast and flexible database interaction with type-safe models.

    ```python
    class User(UserBase, table=True):
        __tablename__ = "users"  # type: ignore
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        hashed_password: str
        created_at: datetime = Field(
            default=None, sa_column_kwargs={"server_default": func.now()}
        )
        updated_at: datetime = Field(
            default=None,
            sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
        )
    ```

- **PostgreSQL**: Robust relational database used for persistent data storage.

- [**CLI Tools**](template_project/cli.py#L10): Command-line interface (CLI) built with
Click to easily manage and automate tasks like running migrations, starting services, etc.

    ```python
    import click

    @click.group()
    def cli():
        pass

    @cli.command()
    def example():
        print("Example command")
    ```

- [**Secrets Management**](template_project/secrets.py#L30): AWS Secrets Manager is used for securely handling sensitive
information (e.g., database credentials).

    ```python
    class SecretDatabaseSettings(SecretBaseSettings):
        model_config = SettingsConfigDict(env_prefix='PG_')
        USER: str
        PASSWORD: str
    ```

- [**Authentication & Security**](template_project/api/auth.py#L11): Token-based
authentication using JWT, ensuring secure and stateless communication between clients
and the backend, as well as [custom token authentication](template_project/api/auth.py#L37)
for administrative API calls and service to service communication.

- **Separation of Concerns**: Enforce a clean architecture that separates business
logic, data models, and API routes, facilitating easy maintenance and extensibility.

- **Code Formatting with Black**: Ensures consistent code style across the project by
automatically formatting Python code to follow the PEP 8 standard. Black helps keep the
code clean and readable with minimal configuration, promoting a uniform development environment.

- **Database Migrations**: Seamless database schema management and migrations using Alembic.

- [**Dockerized**](Dockerfile): Fully containerized with Docker for simplified deployment and
development workflows.

- [**Docker Compose**](docker-compose.yaml): The project uses Docker Compose for easy setup and management of
the application and its dependencies, ensuring a consistent environment.

</details>

<details open>
    <summary><h2>Code Structure</h2></summary>

```
.
├── Dockerfile
├── README.md
├── alembic.ini
├── migrations
│   ├── README.md
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── ...
├── requirements.txt
├── setup.py
└── template_project
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── auth.py
    │   ├── cache.py
    │   ├── cli.py
    │   ├── dependencies.py
    │   ├── exceptions.py
    │   ├── factories.py
    │   └── routers
    │       ├── __init__.py
    │       ├── accounts.py
    │       └── system.py
    ├── cli.py
    ├── config.py
    ├── db
    │   ├── __init__.py
    │   ├── controllers
    │   │   ├── __init__.py
    │   │   └── accounts.py
    │   └── factories.py
    ├── models
    │   ├── __init__.py
    │   ├── database.py
    │   └── validation.py
    ├── secrets.py
    └── security.py
```
</details>

<details open>
    <summary><h2>Development</h4></summary>


### Prerequisites

#### Python Installation

Ensure Python 3.11 is installed on your machine. Check your Python version by running:

```bash
python --version
```

#### Virtual Environment

Set up and activate a virtual environment with one of the following ways:

##### Using venv

```bash
python -m venv venv
source ./venv/bin/activate
```

##### Using pyenv

```bash
pyenv virtualenv 3.11 template-project
pyenv shell template-project
```

#### Installing Dependencies

To install required packages for the project, execute:

```bash
pip install -r requirements.txt && pip install -e .
```

#### Environment

First, copy `.env.sample` file to `.env` and replace the environment variables
accordingly.

```bash
cp .env.sample .env
```

#### Database

To setup the database for the project:

* 1. Create a database using a database administration tool (e.g. DBeaver)

* 2. Set the environment variables for the database

* 3. Use alembic to setup the schema:

    ```bash
    alembic upgrade head
    ```

#### Running the Application

You can see the available commands and their options by running:

```bash
template-cli --help
```

#### Building the docker image

To build the docker image, run the following command:

```bash
docker build -t project-template:latest .
```

#### Running the Application in Docker

To run the application in a docker container, execute:

```bash
docker run -it --rm project-template:latest template-cli --help
```

To run the api server using docker, execute:

```bash
docker run -it --rm --env-file=.env -p 8000:8000 project-template:latest template-cli api start
```

You can also use docker compose:

```bash
docker compose up
```

You can now access the api interactive documentation at `http://localhost:8000/docs`.

</details>


## Roadmap

* Docstrings:

    Adding docstrings to all functions and classes to improve code readability and
    provide clear documentation for future developers.

* Unit tests:

    Implementing unit tests to ensure code reliability and ease of maintenance. This
    will help catch bugs early and verify that changes don’t break existing functionality.

* HTML template:

    Integrating an HTML template using Jinja for dynamic content rendering, enhancing
    the flexibility and presentation of the application’s user interface.
