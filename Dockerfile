FROM python:3.11-slim-bookworm

# Maintainer and Architecture info
LABEL maintainer="AI Lab Assistant"
LABEL architecture="linux/arm64"

# Set non-interactive to prevent apt prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install necessary hardware audio packages
# Bookworm is the target Debian version for Raspberry Pi OS (PiOS12)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    libsdl2-mixer-2.0-0 \
    flac \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up the internal application directory
WORKDIR /app

# Copy the dependency file
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and the knowledge base folder
COPY src/ /app/src/
COPY data/ /app/data/

# Verify the container is ALSA ready on execution
# Run the voice assistant script
CMD ["sh", "-c", "python3 src/main.py"]
