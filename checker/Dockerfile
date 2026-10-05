FROM python:3.12-slim
WORKDIR /checker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY checker.py .
ENTRYPOINT ["python", "checker.py"]
