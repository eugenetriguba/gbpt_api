ARG ENV

FROM eugenetriguba/python:3.10-poetry1.2

ENV BUILD_DEPS="\
build-essential \
python3-dev \
libssl-dev \
libffi-dev \
cargo"

USER root

COPY --chown=$APP_USER:$APP_USER . /usr/local/src/api
WORKDIR /usr/local/src/api

RUN apt-get update --assume-yes --quiet \
    && apt-get install \
        --assume-yes \
        --quiet \
        --no-install-recommends \
        $BUILD_DEPS \
    && su $APP_USER --command "chmod u+x ./utils/docker_deps_install.sh" \
    && su $APP_USER --command "./utils/docker_deps_install.sh" \
    && apt-get purge -y --auto-remove $BUILD_DEPS

USER $APP_USER
CMD ["/bin/sh"]
