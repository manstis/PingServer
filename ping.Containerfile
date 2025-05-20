FROM registry.access.redhat.com/ubi9/ubi:latest AS production

# Install dependencies
RUN dnf install -y \
    python3.12 \
    python3.12-pip

USER 1000
WORKDIR /var/www

COPY requirements.txt .
COPY main.py .
COPY ping_server.py .
COPY uvicorn_runner.py .

# Compile application
RUN /usr/bin/python3.12 -m venv /var/www/venv
ENV PATH="/var/www/venv/bin:${PATH}"

RUN /var/www/venv/bin/python3.12 -m pip install --no-cache-dir --no-binary=all -r ./requirements.txt

# Launch!
ENTRYPOINT ["python3.12", "ping_server.py"]
CMD ["python3.12", "ping_server.py"]

EXPOSE 8080
