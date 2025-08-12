FROM ollama/ollama:latest

# Install curl for health checks and initialization
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the initialization script
COPY text_to_sql/init_model.sh /usr/local/bin/init_model.sh
RUN chmod +x /usr/local/bin/init_model.sh

# Create a directory for models
RUN mkdir -p /root/.ollama

# Expose the default Ollama port
EXPOSE 11434

# Start Ollama and initialize the model
ENTRYPOINT ["/bin/bash", "-c", "ollama serve & /usr/local/bin/init_model.sh"] 