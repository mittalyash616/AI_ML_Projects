FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but useful for langchain/openai)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY builder/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src

# Set Python path so src is discoverable
ENV PYTHONPATH=/app/src

# Run the handler
CMD ["python3", "-u", "src/handler.py"]
