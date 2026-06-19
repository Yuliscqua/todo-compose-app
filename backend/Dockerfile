FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'API
COPY main.py .

# Exposer le port 5000
EXPOSE 5000

# Lancer l'API avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]