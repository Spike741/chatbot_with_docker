# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if any) or install dependencies
# If you have a requirements.txt, uncomment these lines:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Otherwise, install directly here
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv groq

# Copy app source code
COPY . .

# Expose port (same as uvicorn runs on)
EXPOSE 8000

# Run app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
