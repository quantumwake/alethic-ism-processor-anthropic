# Stage 1: Base Image with Miniconda
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

ARG CONDA_ISM_CORE_PATH
ARG CONDA_ISM_DB_PATH
ARG GITHUB_REPO_URL

# copy the local channel packages (alethic-ism-core, alethic-ism-db)
COPY ${CONDA_ISM_DB_PATH} .
COPY ${CONDA_ISM_CORE_PATH} .

# extract the local channel directories
RUN tar -zxvf $CONDA_ISM_DB_PATH -C /
RUN tar -zxvf $CONDA_ISM_CORE_PATH -C /

# clone the api repo
#RUN git clone --depth 1 ${GITHUB_REPO_URL} repo
ADD . /app/repo

# Move to the repository directory
WORKDIR /app/repo

# Force all commands to run in bash
SHELL ["/bin/bash", "--login", "-c"]

# install the conda build package in base
RUN conda install -y conda-build

# reindex local channel
RUN conda index /app/conda/env/local_channel

# Initialize the conda environment
RUN conda env create -f environment.yaml

# Initialize conda in bash config files:
RUN conda init bash

# Activate the environment, and make sure it's activated:
RUN echo "conda activate alethic-ism-processor-anthropic" > ~/.bashrc

# display information about the current activation
RUN conda info

# Install necessary dependencies for the build process
RUN conda install -y conda-build

#RUN conda clean --all -f -y
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict

## Install Conda packages
RUN conda install -y pulsar-client

# ** this is required for anthropic and pydantic
# ** otherwise anthropic keeps downgrading pydantic to version ~= 1.0 from >=2.0
RUN conda uninstall pydantic --force-remove
# had to hard code the versions for pydantic, 2.5.3 has issues
RUN conda install pydantic==2.5.2 --no-deps -c conda-forge
RUN conda install pydantic-core==2.14.5 -c conda-forge
RUN conda install annotated-types==0.6.0 -c conda-forge


# display all packages installed
RUN conda list

COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["entrypoint.sh"]

# Run the pulsar consumer (ism processor for anthropic)
CMD ["python", "main.py"]

