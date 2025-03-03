# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies and Python 3.11.11
RUN apt-get update && \
#    apt-get install -y \
#    software-properties-common && \
#    add-apt-repository ppa:deadsnakes/ppa && \
#    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify Python version
RUN python3 --version

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["streamlit", "User_interface/ui.py", "run"]

