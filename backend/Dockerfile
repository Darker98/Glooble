# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab
RUN python -m nltk.downloader punkt stopwords

# Copy source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
