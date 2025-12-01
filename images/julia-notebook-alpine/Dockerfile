ARG REGISTRY=ghcr.io
ARG OWNER=pavel-dvlp
ARG BASE_IMAGE_VERSION=0.2
ARG BASE_IMAGE=$REGISTRY/$OWNER/jupiter-docker-stacks/minimal-notebook-alpine:$BASE_IMAGE_VERSION
FROM $BASE_IMAGE

LABEL maintainer="Pavel Krylov <pavel.dvlp@gmail.com>"

USER root
RUN apk update && apk add --no-cache curl
RUN pip install --break-system-packages --no-cache-dir --compile \
    requests

COPY setup_julia.py /opt/setup-scripts/

RUN fix-permissions /opt/setup-scripts/ && \
    chmod a+rx /opt/setup-scripts/setup_julia.py

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

RUN pip install --break-system-packages --no-cache-dir --compile \
    plotly \
    kaleido \
    anywidget \
    numpy \
    jupyter_contrib_nbextensions \
    webio_jupyter_extension

COPY setup-julia-packages.sh /opt/setup-scripts/

RUN chmod a+rx /opt/setup-scripts/setup-julia-packages.sh 

USER ${NB_UID}

RUN /opt/setup-scripts/setup-julia-packages.sh

