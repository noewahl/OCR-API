FROM python:3.12.7-slim

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    wget \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    ninja-build \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Set environment variables for llama-cpp-python build
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS -DCMAKE_C_FLAGS='-march=armv8-a' -DCMAKE_CXX_FLAGS='-march=armv8-a'"
ENV FORCE_CMAKE=1

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Create models directory and download LLaMA model
RUN mkdir -p models && \
    wget -O models/llama-2-7b-chat.Q4_K_M.gguf \
    "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD ["python", "app.py"]