FROM python:3.8.1-alpine3.11

MAINTAINER "Amit Panda <amitpanda007@gmail.com>"

RUN apk update \
    && apk add --upgrade --no-cache \
        bash openssh curl ca-certificates openssl less htop \
        g++ make wget rsync \
        build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
        libgcc libquadmath musl \
        libgfortran \
        lapack-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --upgrade cython \
    && pip install numpy==1.17.3 \
    && pip install scipy==1.3.1

WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]