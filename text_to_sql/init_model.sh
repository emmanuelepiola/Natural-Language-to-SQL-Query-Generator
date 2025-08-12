#!/bin/bash

echo "Waiting for Ollama service to start..."

# Wait for Ollama service to be ready
while ! curl -f http://localhost:11434/api/tags >/dev/null 2>&1; do
    sleep 2
done

echo "Ollama service is ready. Pulling gemma3:1b-it-qat model..."

# Pull the Gemma 1B instruction-tuned quantized model
ollama pull gemma3:1b-it-qat

echo "Model gemma3:1b-it-qat pulled successfully!"

# Keep the container running
tail -f /dev/null 