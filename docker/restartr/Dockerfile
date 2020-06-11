######################################################
#
# A container for the core semantic-search capability.
#
######################################################
FROM python:3.7.6-slim 

# Least privilege: Run as a non-root user.
ENV USER restartr
ENV HOME /home/$USER
WORKDIR $HOME
ENV UID 1000
RUN adduser --disabled-login --home $HOME --shell /bin/bash --uid $UID $USER && \
   chown -R $UID:$UID $HOME

# Install source code and required packages.
# Run restartr to also install KGX.
RUN \
    apt update && \
        apt-get install -y curl gettext git gcc && \
        git clone https://github.com/helxplatform/restartr.git && \
        cd restartr && \
        pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt && \
        find . -type f -exec chmod 664 {} \; && \
        find . -type f -iname *.py -exec chmod 775 {} \; && \
        find bin -type f -exec chmod 775 {} \; && \
        find . -type d -exec chmod 775 {} \; && \
        rm -rf /var/cache/apk/* &&
            \
	apt-get remove -y --purge  git

USER $USER
ENV PYTHONPATH $HOME/restartr
ENV API_KEY 439598345702938570239
ENV MONGO_USERNAME root
ENV MONGO_PASSWORD example
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
WORKDIR $HOME/restartr
RUN  rm  -rf data docker kubernetes
# Define the entrypoint.
ENTRYPOINT bin/restartr api
