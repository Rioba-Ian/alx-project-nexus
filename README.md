# ALX Project Nexus: A ProDev Backend Engineering Journey

ALX Project Nexus documentation. This project's purpose is to document key learning areas and milestones of the ALX ProBackend Engineering Journey.

## Developing a Backend for a Job Board Platform - ProDev BE

This project creates a jobs board listing that allows users to access, filter and search job postings. It implements Role-Based Access Control (RBAC) where admins can post jobs and users can only view and apply to these jobs. Users can apply for jobs and bookmark/save applications for future reference. The aim of this project is to demonstrate role-based access control as well as robust API design. It is built using Django and PostgreSQL for the database, containerized with Docker.

### Table of Contents

- [ALX Project Nexus: A ProDev Backend Engineering Journey](#alx-project-nexus-a-prodev-backend-engineering-journey)
  - [Developing a Backend for a Job Board Platform - ProDev BE](#developing-a-backend-for-a-job-board-platform---prodev-be)
    - [Table of Contents](#table-of-contents)
    - [Key Technologies](#key-technologies)
    - [Features](#features)
    - [Learning Areas](#learning-areas)
    - [Backend Development with Django](#backend-development-with-django)
    - [API Design and REST Best Practices](#api-design-and-rest-best-practices)
    - [Authentication and Authorization](#authentication-and-authorization)
    - [Database Design and Management](#database-design-and-management)
    - [Docker and Containerization](#docker-and-containerization)
    - [API Documentation](#api-documentation)
    - [CI/CD Pipeline](#cicd-pipeline)
      - [Pipeline Features](#pipeline-features)
      - [Workflow Steps](#workflow-steps)
    - [Setup and Installation](#setup-and-installation)
    - [Deployment Options](#deployment-options)
    - [Contributing](#contributing)
    - [License](#license)

### Key Technologies

- Python 3
- Django & Django REST Framework
- JWT Authentication
- PostgreSQL
- Docker & Docker Compose
- Swagger/OpenAPI for documentation

### Features

- User authentication with JWT tokens
- Role-based access control (Admin/User roles)
- Job listing creation and management
- RESTful API design
- Comprehensive API documentation
- Containerized development environment

### Learning Areas

#### Backend Development with Django

- Creating custom user models that extend Django's built-in authentication
- Implementing custom permission classes for fine-grained access control
- Using Django's ORM for efficient database interactions
- Developing modular applications with Django's app architecture
- Implementing custom model managers and methods

#### API Design and REST Best Practices

- Designing a RESTful API with proper endpoint naming conventions
- Implementing proper status codes and response formatting
- Using serializers for data validation and transformation
- Pagination for handling large datasets
- Filtering and searching capabilities

#### Authentication and Authorization

- JWT-based authentication flow with token refresh capabilities
- Role-based access control implementation
- Permission-based endpoint protection
- Secure password handling and validation

#### Database Design and Management

- Relational database design with PostgreSQL
- Django migrations for schema evolution
- Foreign key relationships and constraints
- Efficient querying and optimization

#### Docker and Containerization

- Multi-container application setup with Docker Compose
- Environment configuration management
- Volume management for persistent data
- Docker networking between services

#### API Documentation

- Auto-generated API documentation with Swagger/OpenAPI
- Interactive documentation endpoints
- Testing API endpoints through documentation interface

#### CI/CD Pipeline

The project includes a fully automated CI/CD pipeline using GitHub Actions that builds, tests, and deploys the application.

##### Pipeline Features

- Automated build and deployment pipeline using GitHub Actions
- Continuous integration with automated testing
- Docker image building and pushing to Docker Hub
- Multi-stage build process for optimized images
- Automatic deployment to production on successful builds
- Versioned Docker images with meaningful tags
- Health checks for all containerized services
- Production-ready Docker Compose configuration

##### Workflow Steps

1. **Build**: Compiles the application and creates Docker images
2. **Test**: Runs automated tests to ensure code quality
3. **Push**: Uploads images to Docker Hub with appropriate tags
4. **Deploy**: Automatically deploys to the production environment

### Setup and Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/alx-project-nexus.git
   cd alx-project-nexus
   ```

2. Create a `.env` file with the necessary environment variables (see `.env.example`)

3. Build and run the containers:

   ```
   docker-compose up --build
   ```

4. Access the application:
   - API: http://localhost:8000/api/
   - Admin interface: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/swagger/

### CI/CD Pipeline Setup

The project includes a GitHub Actions workflow for CI/CD that automatically builds, tests, and deploys the application.

#### Setting Up GitHub Secrets

1. In your GitHub repository, go to Settings > Secrets and Variables > Actions > New repository secret

2. Add the following secrets:

   | Secret Name       | Description                                                   | Example                                                                       |
   | ----------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
   | `DOCKER_USERNAME` | Your Docker Hub username                                      | `yourusername`                                                                |
   | `DOCKER_PASSWORD` | Docker Hub password or access token (recommended)             | `dckr_pat_abcdefghijklmnopqrstuvwxyz`                                         |
   | `SSH_PRIVATE_KEY` | Your deployment server's SSH private key (the entire content) | `-----BEGIN OPENSSH PRIVATE KEY-----\n...\n-----END OPENSSH PRIVATE KEY-----` |
   | `SSH_USER`        | Username for the deployment server                            | `ubuntu` or `root`                                                            |
   | `DEPLOY_HOST`     | Hostname or IP address of your deployment server              | `123.456.789.0`                                                               |

#### Creating SSH Keys for Deployment

To generate a new SSH key for your deployment:

1. Generate a new SSH key pair:

   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
   ```

2. Add the public key to your server's `authorized_keys`:

   ```bash
   cat ~/.ssh/github_actions_deploy.pub
   # Copy the output and add it to ~/.ssh/authorized_keys on your server
   ```

3. Add the private key as a GitHub secret:

   ```bash
   cat ~/.ssh/github_actions_deploy
   # Copy the entire output (including BEGIN and END lines) to the SSH_PRIVATE_KEY secret
   ```

4. Ensure the correct permissions on your server:
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

#### Workflow Triggers

The workflow will trigger automatically on:

- Pushes to the main branch
- New version tags (v1.0.0, v2.1.3, etc.)
- Manual workflow dispatch

For manual triggers, you can use the "Run workflow" button in the Actions tab of your GitHub repository.

#### Troubleshooting Deployment

If you encounter SSH connection issues during deployment:

1. Verify your `SSH_PRIVATE_KEY` format is correct (including newlines)
2. Check that the public key is properly added to `~/.ssh/authorized_keys` on your server
3. Ensure your server's SSH configuration allows key-based authentication
4. Verify that your `SSH_USER` has the necessary permissions on the server
5. Check firewall settings to ensure port 22 is accessible

### Deployment Options

The project supports multiple deployment options:

1. **Local Development**:

   ```
   docker-compose up
   ```

2. **Production Deployment**:

   ```
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Automated Deployment via CI/CD**:
   - Push to the main branch or create a new version tag
   - GitHub Actions will automatically deploy to your server

4. **Manual Production Setup**:
   - Copy `.env.prod.example` to `.env.prod` and configure
   - Copy `.env.prod.db.example` to `.env.prod.db` and configure
   - Run with the production compose file

### Contributing

I hope to bring the UI to life! You can easily contribute by:

1. Forking the repository
2. Creating a feature branch (`git checkout -b feature/amazing-feature`)
3. Committing your changes (`git commit -m 'Add some amazing feature'`)

4. Pushing to the branch (`git push origin feature/amazing-feature`)
5. Opening a Pull Request

### License

MIT License
