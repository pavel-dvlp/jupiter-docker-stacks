ARG REGISTRY=ghcr.io
ARG OWNER=pavel-dvlp
ARG BASE_IMAGE_VERSION=0.1
ARG BASE_IMAGE=$REGISTRY/$OWNER/jupiter-docker-stacks/minimal-notebook-alpine:$BASE_IMAGE_VERSION
FROM $BASE_IMAGE

LABEL maintainer="Pavel Krylov <pavel.dvlp@gmail.com>"

COPY setup_julia.py setup-julia-packages.sh /opt/setup-scripts/

USER root
RUN fix-permissions /opt/setup-scripts/ && \
    chmod a+rx /opt/setup-scripts/setup_julia.py && \
    chmod a+rx /opt/setup-scripts/setup-julia-packages.sh

RUN apk update && apk add --no-cache \
    curl

# Julia dependencies
# install Julia packages in /opt/julia instead of ${HOME}
ENV JULIA_DEPOT_PATH=/opt/julia \
    JULIA_PKGDIR=/opt/julia \
    JULIA_VERSION=1.10.10

# Setup Julia
RUN /opt/setup-scripts/setup_julia.py

# macOS Rosetta virtualization creates junk directory which gets owned by root further up.
# It'll get re-created, but as USER runner after the next directive so hopefully should not cause permission issues.
#
# More info: https://github.com/jupyter/docker-stacks/issues/2296
# hadolint ignore=DL3059
RUN rm -rf "/home/${NB_USER}/.cache/"

USER ${NB_UID}

# Setup IJulia kernel & other packages
RUN /opt/setup-scripts/setup-julia-packages.sh