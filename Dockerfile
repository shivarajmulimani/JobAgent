# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies and Python 3.11.11
# Install dependencies
RUN apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip curl && \
    apt-get install -y xfonts-75dpi xfonts-base libjpeg-turbo8 libxrender1 libxext6 libfontconfig1 && \
    curl -L -o wkhtmltox.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.jammy_amd64.deb && \
    dpkg -i wkhtmltox.deb || apt-get -f install -y && \
    rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify Python version
RUN python3 --version

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["streamlit", "run", "User_interface/ui.py"]

