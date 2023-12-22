# Alethic Instruction-Based State Machine (Anthropic Processor)

The following processor waits on events from pulsar (but can be extended to use kafka or any pub/sub system)

- conda config --add channels /Users/kasrarasaee/miniconda3/envs/local_channel
- conda config --show channels

# initialize the environment
- conda env create -f environment.yaml
- conda activate alethic-ism-processor-anthropic

# Installation
- conda install pulsar-client
- conda install annotated-types
- conda install pydantic                          # should work on non apple silicon? not tested
- conda install python-dotenv
- conda install anthropic (>=0.7.8)
- conda install tenacity
- conda install pyyaml
- conda install psycopg2


Troubleshoot pydantic and anthropic version issues (observed on apple silicon with m3 max):
check pydantic version after installing anthropic on apple silicon (version >=2.5), 
in some cases, in a newly created conda environment and project, installing anthropic 
on an Apple Silicon (osx-arm64) system downgrades pydantic to version==1

Option 1 (freeze the version to >2 but this may also cause anthropic to revert to older versions <=0.2)
- conda install pydantic==2.5.3 -c conda-forge    # anthropic is picking v1 on apple silicon
- conda install pydantic-core==2.14.6 -c conda-forge
- 
Option 2 (uninstall it and force a no dependency check install - seems to work on an apple m3)
- conda uninstall pydantic --force-remove
- conda install pydantic --no-deps
- conda install annotated-types

# Remote Alethic Dependencies (if avail otherwise build locally)
- conda install alethic-ism-core
- conda install alethic-ism-db

# Local Dependency (build locally if not using remote channel)
- conda install -c ~/miniconda3/envs/local_channel alethic-ism-core
- conda install -c ~/miniconda3/envs/local_channel alethic-ism-db

