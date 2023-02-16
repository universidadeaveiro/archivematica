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
COPY src/MCPClient/osdeps /src/src/MCPClient/osdeps
RUN set -ex \
	&& curl -s https://packages.archivematica.org/GPG-KEY-archivematica | apt-key add - \
	&& add-apt-repository --no-update --yes "deb [arch=amd64] http://packages.archivematica.org/1.13.x/ubuntu-externals bionic main" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic multiverse" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-security universe" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-updates multiverse" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential libyaml-dev \
	&& /src/hack/osdeps.py Ubuntu-18 1 MCPClient | grep -v -E "nginx|postfix" | xargs apt-get install -y --no-install-recommends \
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
COPY ./src/MCPClient /src/src/MCPClient

# MCP Client

# Some scripts in archivematica-fpr-admin executed by MCPClient rely on certain
# files being available in this image (e.g. see https://git.io/vA1wF).
COPY src/archivematicaCommon/lib/externals/fido/ /usr/lib/archivematica/archivematicaCommon/externals/fido/
COPY src/archivematicaCommon/lib/externals/fiwalk_plugins/ /usr/lib/archivematica/archivematicaCommon/externals/fiwalk_plugins/

COPY hack/entrypoints/mcp-client-entrypoint.sh /

#USER archivematica

ENV DJANGO_SETTINGS_MODULE settings.common
ENV PYTHONPATH /src/src/MCPClient/lib/:/src/src/MCPClient/lib/clientScripts:/src/src/archivematicaCommon/lib/:/src/src/dashboard/src/
ENV ARCHIVEMATICA_MCPCLIENT_ARCHIVEMATICACLIENTMODULES /src/src/MCPClient/lib/archivematicaClientModules
ENV ARCHIVEMATICA_MCPCLIENT_CLIENTASSETSDIRECTORY /src/src/MCPClient/lib/assets/
ENV ARCHIVEMATICA_MCPCLIENT_CLIENTSCRIPTSDIRECTORY /src/src/MCPClient/lib/clientScripts/

ENTRYPOINT ["sh", "/mcp-client-entrypoint.sh"]