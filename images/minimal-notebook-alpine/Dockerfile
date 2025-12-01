# Alpine 3.22
# https://hub.docker.com/_/alpine

ARG ROOT_IMAGE=frolvlad/alpine-glibc:alpine-3.22
# ARG ROOT_IMAGE=alpine:3.22

FROM $ROOT_IMAGE

LABEL maintainer="Pavel Krylov <pavel.dvlp@gmail.com>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
# SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for the Server that starts
# but lacks all features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND=noninteractive
RUN apk update && apk add --no-cache \
    # - bzip2 is necessary to extract the micromamba executable.
    bzip2 \
    ca-certificates \
    musl-locales \
    sudo \
    # - `tini` is installed as a helpful container entrypoint,
    #   that reaps zombie processes and such of the actual executable we want to start
    #   See https://github.com/krallin/tini#why-tini for details
    tini \
    wget

# RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen 
# RUN echo "C.UTF-8 UTF-8" >> /etc/locale.gen
# RUN locale-gen

# Configure environment
ENV NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8
ENV HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Delete existing user with UID="${NB_UID}" if it exists
# hadolint ignore=SC2046
RUN if grep -q "${NB_UID}" /etc/passwd; then \
        userdel --remove $(id -un "${NB_UID}"); \
    fi

# Create "${NB_USER}" user (`jovyan` by default) with UID="${NB_UID}" (`1000` by default) and in the 'users' group
# and make sure these dirs are writable by the `users` group.
# RUN echo 'auth requisite pam_deny.so' >> /etc/pam.d/su
RUN sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers
RUN sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers
# -D for no password
RUN adduser -s /bin/sh -u "${NB_UID}" -D -G users "${NB_USER}" 
RUN chmod g+w /etc/passwd 

# macOS Rosetta virtualization creates junk directory which gets owned by root further up.
# It'll get re-created, but as USER runner after the next directive so hopefully should not cause permission issues.
#
# More info: https://github.com/jupyter/docker-stacks/issues/2296
RUN rm -rf "/home/${NB_USER}/.cache/"

RUN apk add --no-cache \
    # - bzip2 is necessary to extract the micromamba executable.
    python3 \
    py3-pip \
    py3-psutil

RUN pip install --break-system-packages --no-cache-dir --compile \
    notebook==6.5.7

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && mkdir "/home/${NB_USER}/.jupyter"

ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

COPY jupyter_notebook_config.py docker_healthcheck.py /etc/jupyter/
RUN cp /etc/jupyter/jupyter_notebook_config.py "/home/${NB_USER}/.jupyter"

RUN fix-permissions /etc/jupyter/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server`, and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=3s --timeout=1s --start-period=3s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1


WORKDIR "${HOME}"

RUN fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

CMD jupyter notebook
