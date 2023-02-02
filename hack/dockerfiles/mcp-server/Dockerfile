FROM ubuntu:18.04 AS base

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN set -ex \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		apt-transport-https \
		curl \
		gettext \
		git \
		gpg-agent \
		locales \
		software-properties-common \
	&& rm -rf /var/lib/apt/lists/*

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# OS dependencies
COPY hack/osdeps.py /src/hack/osdeps.py
COPY src/MCPServer/osdeps /src/src/MCPServer/osdeps
RUN set -ex \
	&& curl -s https://packages.archivematica.org/GPG-KEY-archivematica | apt-key add - \
	&& add-apt-repository --no-update --yes "deb [arch=amd64] http://packages.archivematica.org/1.13.x/ubuntu-externals bionic main" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic multiverse" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-security universe" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-updates multiverse" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential libyaml-dev \
	&& /src/hack/osdeps.py Ubuntu-18 1 MCPServer | grep -v -E "nginx|postfix" | xargs apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN set -ex \
	&& groupadd --gid 333 --system archivematica \
	&& useradd -m --uid 333 --gid 333 --system archivematica

RUN set -ex \
	&& mkdir -p /var/archivematica/sharedDirectory \
	&& chown -R archivematica:archivematica /var/archivematica

# Python 3
COPY requirements-py3.txt /src/requirements-py3.txt

RUN set -ex \
	&& curl -s https://bootstrap.pypa.io/pip/3.6/get-pip.py | python3.6 \
	&& update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
	&& pip3 install -r /src/requirements-py3.txt

COPY ./src/archivematicaCommon /src/src/archivematicaCommon
COPY ./src/dashboard /src/src/dashboard
COPY ./src/MCPServer /src/src/MCPServer

# MCP Server

COPY hack/entrypoints/mcp-server-entrypoint.sh /

RUN set -ex \
	chmod +x /mcp-server-entrypoint.sh


ENV DJANGO_SETTINGS_MODULE settings.common
ENV PYTHONPATH /src/src/MCPServer/lib/:/src/src/archivematicaCommon/lib/:/src/src/dashboard/src/

ENTRYPOINT ["sh", "mcp-server-entrypoint.sh"]