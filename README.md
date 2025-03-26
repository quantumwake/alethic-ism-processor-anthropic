# Alethic Instruction-Based State Machine (Anthropic Processor)

## Overview
A processor module for the Alethic ISM that handles Anthropic AI model interactions. 

This processor:
- Accepts input states and their associated instructions and state configutation.
- Processes inputs through Anthropic's AI models, returning results and future processing instructions.
- Outputs states containing derived results and forwards them back onto the ISM network.
- Ensures type compatibility with connected processors.

## Build Docker Image

```bash
make docker
```

## Environment Initialization
- Create environment: `conda env create -f environment.yaml`.
- Activate environment: `conda activate alethic-ism-processor-anthropic`.

## Troubleshooting
For pydantic and anthropic version issues on Apple Silicon (M3 Max):
- Force remove pydantic: `conda uninstall pydantic --force-remove`.
- Reinstall pydantic without dependencies: `conda install pydantic --no-deps`.
- Install annotated-types: `conda install annotated-types`.

## Alethic Dependencies
- `conda install quantumwake::alethic-ism-core`
- `conda install quantumwake::alethic-ism-db`

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
