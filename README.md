# Alethic Instruction-Based State Machine (Anthropic Processor)

This processor module is designed to respond to events from Pulsar and can be extended to other pub/sub systems like Kafka.

## Setup and Configuration
If you are using miniconda, something along the lines of:
- Add Conda channel: `conda config --add channels ~/miniconda3/envs/local_channel`.
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
For pydantic and anthropic version issues on Apple Silicon (M3 Max):
- Force remove pydantic: `conda uninstall pydantic --force-remove`.
- Reinstall pydantic without dependencies: `conda install pydantic --no-deps`.
- Install annotated-types: `conda install annotated-types`.

## Alethic Dependencies
- Remote: `conda install alethic-ism-core`, `conda install alethic-ism-db`.
- Local: Install from the local channel if remote versions aren't available.

## Testing
- ** testing is not exactly working right now **
- Install pytest: `conda install pytest`.

## Contribution
Contributions, questions, and feedback are highly encouraged. Contact us for any queries or suggestions.

## License
Released under GNU3 license.

## Acknowledgements
Special thanks to Alethic Research, Princeton University Center for Human Values, and New York University.

---

For more updates and involvement opportunities, visit the [Alethic ISM GitHub page](https://github.com/quantumwake/alethic) or create an issue/comment ticket.
