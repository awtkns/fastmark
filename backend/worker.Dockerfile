FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
  && apt-get install -y \
    build-essential \
    cmake \
    libgoogle-glog-dev \
    libgflags-dev \
    libgtest-dev \
    python3.8 \
    python3-pip \
  && apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .
CMD ["uvicorn", "asgi:application", "--host", "0.0.0.0", "--port", "5000", "--reload"]
