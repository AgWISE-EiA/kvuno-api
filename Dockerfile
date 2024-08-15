# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Update the package list and install net-tools
RUN apt-get update && apt-get install -y net-tools

RUN mkdir /app

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject-old.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock /app/

# Install project dependencies using Poetry
RUN poetry install

# generate thr requirements.txt

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . /app


# Make port 80 available to the world outside this container
EXPOSE 5000

# Define the command to run your Flask app
#CMD [ "poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0" ]
CMD ["gunicorn", "-c", "app/gunicorn_config.py", "wsgi:app"]