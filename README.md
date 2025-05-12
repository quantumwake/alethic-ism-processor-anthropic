# Alethic Instruction-Based State Machine (Anthropic Processor)

The Alethic ISM Anthropic Processor is a component of the Alethic Instruction-Based State Machine framework, specifically designed to process instructions using Anthropic's language models. This processor interfaces with the Anthropic API to provide language model capabilities within the ISM ecosystem.

## Overview

This processor is part of a larger state machine architecture, designed to efficiently handle and route messages through a system of interconnected processors. It integrates with NATS for messaging and PostgreSQL for state storage.

## Features

- Integration with Anthropic's language models
- Message processing and state management
- NATS-based messaging system
- PostgreSQL state persistence
- Containerized deployment with Docker
- Kubernetes deployment support
- GitHub Actions CI/CD pipeline

## Requirements

- Python 3.12+
- uv package manager
- PostgreSQL database
- NATS server
- Anthropic API key

## Installation

### Local Development

```shell
# Install uv package manager
pip install uv

# Set up virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Docker Build

Use the provided script to build the Docker image:

```shell
sh docker_build.sh -i krasaee/alethic-ism-processor-anthropic:latest
```

Additional build options:
- `-p` - Specify platform architecture (default: linux/amd64)
- `-b` - Use buildpack instead of direct Docker build

## Configuration

The application is configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| ANTHROPIC_API_KEY | Anthropic API key for accessing their models | Required |
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres1@localhost:5432/postgres |
| ROUTING_FILE | Path to the YAML routing configuration | .routing.yaml |
| LOG_LEVEL | Logging level | INFO |

## Deployment

### Docker

Run the container with the following command:

```shell
docker run -d \
  --name alethic-ism-processor-anthropic \
  -e ANTHROPIC_API_KEY="your_api_key_here" \
  -e LOG_LEVEL=DEBUG \
  -e ROUTING_FILE=/app/repo/.routing.yaml \
  -e DATABASE_URL="postgresql://postgres:postgres1@host.docker.internal:5432/postgres" \
  krasaee/alethic-ism-processor-anthropic:latest
```

### Kubernetes

Deploy to Kubernetes using the provided deployment script:

```shell
sh docker_deploy.sh -i krasaee/alethic-ism-processor-anthropic:latest
```

The Kubernetes deployment requires the following secrets:
- `alethic-ism-processor-anthropic-secret`: Contains environment variables
- `alethic-ism-routes-secret`: Contains routing configuration

## CI/CD

The repository includes GitHub Actions workflows for automated build, test, and deployment:

- `build-main.yml`: Builds and pushes the Docker image when changes are pushed to the main branch
- `build-release.yml`: Builds, releases, and deploys to Kubernetes when a new version tag is pushed

## Development

### Makefile Commands

```shell
# Build Docker image
make build

# Create a new version tag
make version

# Clean Docker system
make clean

# Display help
make help
```

### Docker Scripts

- `docker_build.sh`: Build the Docker image
- `docker_push.sh`: Push the image to a registry
- `docker_deploy.sh`: Deploy to Kubernetes

## License

Alethic ISM is under a DUAL licensing model:

**AGPL v3**  
Intended for academic, research, and nonprofit institutional use. As long as all derivative works are also open-sourced under the same license, you are free to use, modify, and distribute the software.

**Commercial License**  
Intended for commercial use, including production deployments and proprietary applications. This license allows for closed-source derivative works and commercial distribution. Please contact us for more information.

See [LICENSE](LICENSE.md) and [OSS-LICENSE](OSS-LICENSE.md) for more details.