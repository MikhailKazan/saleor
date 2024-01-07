### Build and install packages
FROM python:3.9 as build-python

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# COPY requirements.txt /app/
WORKDIR /app
## sphinxcontrib-applehelp installed due to https://github.com/saleor/saleor/issues/11664
#RUN pip install sphinxcontrib-applehelp==1.0.2
#RUN pip install -r requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install poetry==1.7.0
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN --mount=type=cache,mode=0755,target=/root/.cache/pypoetry poetry install --no-root

### Debug image
#FROM python:3.9-slim as debug
#
#RUN groupadd -r saleor && useradd -r -g saleor saleor
#
#RUN apt-get update \
#  && apt-get install -y \
#  libcairo2 \
#  libgdk-pixbuf2.0-0 \
#  liblcms2-2 \
#  libopenjp2-7 \
#  libpango-1.0-0 \
#  libpangocairo-1.0-0 \
#  libssl1.1 \
#  libtiff5 \
#  libwebp6 \
#  libxml2 \
#  libpq5 \
#  shared-mime-info \
#  mime-support \
#  gettext \
#  libpq-dev \
#  openssh-server \
#  whois \
##  && apt purge -y whois \
#  && apt -y autoremove \
#  && apt -y autoclean \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/*
#
#
#RUN mkdir -p /app/media /app/static \
#  && chown -R saleor:saleor /app/
#
#COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
#COPY --from=build-python /usr/local/bin/ /usr/local/bin/
#COPY . /app
#WORKDIR /app
#
#ARG STATIC_URL
#ENV STATIC_URL ${STATIC_URL:-/static/}
#RUN SECRET_KEY=dummy STATIC_URL=${STATIC_URL} python3 manage.py collectstatic --no-input
#
#EXPOSE 8000
#EXPOSE 22
#
#ENV PYTHONUNBUFFERED 1
#
#ARG COMMIT_ID
#ARG PROJECT_VERSION
#ENV PROJECT_VERSION="${PROJECT_VERSION}"
#
## >>> SSH Server
#ARG SSHUSERNAME
#ARG SSHUSERPASS
#
## Add a non-root user & set password
#RUN useradd -ms /bin/bash $SSHUSERNAME
#
## Set password for non-root user
#RUN usermod --password $(echo "$SSHUSERPASS" | mkpasswd -s) $SSHUSERNAME
#
#USER $SSHUSERNAME
#RUN mkdir /home/$SSHUSERNAME/.ssh && touch /home/$SSHUSERNAME/.ssh/authorized_keys
#
##USER root
##RUN echo 'root:Grettly8' | chpasswd
##RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
##RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
##RUN echo "export VISIBLE=now" >> /etc/profile
#
#VOLUME /home/$SSHUSERNAME/.ssh
#VOLUME /etc/ssh
## <<< SSH Server
#
#LABEL org.opencontainers.image.title="mirumee/saleor"                                  \
#      org.opencontainers.image.description="\
#A modular, high performance, headless e-commerce platform built with Python, \
#GraphQL, Django, and ReactJS."                                                         \
#      org.opencontainers.image.url="https://saleor.io/"                                \
#      org.opencontainers.image.source="https://github.com/saleor/saleor"               \
#      org.opencontainers.image.revision="$COMMIT_ID"                                   \
#      org.opencontainers.image.version="$PROJECT_VERSION"                              \
#      org.opencontainers.image.authors="Saleor Commerce (https://saleor.io)"           \
#      org.opencontainers.image.licenses="BSD 3"
#
#RUN service ssh start
#
#RUN echo "gunicorn --bind :8000" \
#         "--workers 4" \
#         "--worker-class saleor.asgi.gunicorn_worker.UvicornWorker" \
#         "saleor.asgi:application \n" > runscript.sh
#
#RUN chmod +x ./runscript.sh
#
#CMD ./runscript.sh
## CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "saleor.asgi.gunicorn_worker.UvicornWorker", "saleor.asgi:application"]


### Final image
FROM python:3.9-slim as prod

RUN groupadd -r saleor && useradd -r -g saleor saleor

RUN apt-get update \
  && apt-get install -y \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  liblcms2-2 \
  libopenjp2-7 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libssl3 \
  libtiff6 \
  libwebp7 \
  libxml2 \
  libpq5 \
  shared-mime-info \
  mime-support \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN echo 'image/webp webp' >> /etc/mime.types

RUN mkdir -p /app/media /app/static \
  && chown -R saleor:saleor /app/

COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app

ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}
#RUN SECRET_KEY=dummy STATIC_URL=${STATIC_URL} python3 manage.py collectstatic --no-input

EXPOSE 8000
ENV PYTHONUNBUFFERED 1

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PROJECT_VERSION="${PROJECT_VERSION}"

LABEL org.opencontainers.image.title="mirumee/saleor"                                  \
      org.opencontainers.image.description="\
A modular, high performance, headless e-commerce platform built with Python, \
GraphQL, Django, and ReactJS."                                                         \
      org.opencontainers.image.url="https://saleor.io/"                                \
      org.opencontainers.image.source="https://github.com/saleor/saleor"               \
      org.opencontainers.image.revision="$COMMIT_ID"                                   \
      org.opencontainers.image.version="$PROJECT_VERSION"                              \
      org.opencontainers.image.authors="Saleor Commerce (https://saleor.io)"           \
      org.opencontainers.image.licenses="BSD 3"

CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "saleor.asgi.gunicorn_worker.UvicornWorker", "saleor.asgi:application"]
