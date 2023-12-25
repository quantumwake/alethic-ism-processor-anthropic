# Alethic Instruction-Based State Machine (Anthropic Processor)

This processor module is designed to respond to events from Pulsar and can be extended to other pub/sub systems like Kafka.

## Setup and Configuration
- Add Conda channel: `conda config --add channels /Users/kasrarasaee/miniconda3/envs/local_channel`.
- Show Conda channels: `conda config --show channels`.

## Environment Initialization
- Create environment: `conda env create -f environment.yaml`.
- Activate environment: `conda activate alethic-ism-processor-anthropic`.

## Installation
Install necessary packages including Pulsar client, Pydantic, Python-dotenv, Anthropic, and others:
- `conda install pulsar-client`
- `conda install annotated-types`
- `conda install pydantic` (Check compatibility on Apple Silicon)
- `conda install python-dotenv`
- `conda install anthropic (>=0.7.8)`
- `conda install tenacity`
- `conda install pyyaml`
- `conda install psycopg2`

## Troubleshooting
- Address potential pydantic and anthropic version issues on Apple Silicon.
- Options include version freezing or no-dependency check installs.

## Alethic Dependencies
- Remote: `conda install alethic-ism-core`, `conda install alethic-ism-db`.
- Local: Install from the local channel if remote versions aren't available.

Stay tuned for updates and more information.
