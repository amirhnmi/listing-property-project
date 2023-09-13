FROM python:3.10.6
WORKDIR /main
COPY . /main
COPY ./ requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn","config:app","--host","127.0.0.1","--port","3000"]
