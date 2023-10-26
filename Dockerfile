# pull official base image
FROM python:3.6

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/
# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-dependencies transformers
RUN pip install filelock huggingface-hub numpy packaging pyyaml regex requests tqdm sacremoses
RUN pip install -r requirements.txt
