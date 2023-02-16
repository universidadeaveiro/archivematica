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
COPY src/dashboard/osdeps /src/src/dashboard/osdeps
RUN set -ex \
	&& curl -s https://packages.archivematica.org/GPG-KEY-archivematica | apt-key add - \
	&& add-apt-repository --no-update --yes "deb [arch=amd64] http://packages.archivematica.org/1.13.x/ubuntu-externals bionic main" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic multiverse" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-security universe" \
	&& add-apt-repository --no-update --yes "deb http://archive.ubuntu.com/ubuntu/ bionic-updates multiverse" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential libyaml-dev \
	&& /src/hack/osdeps.py Ubuntu-18 1 dashboard | grep -v -E "nginx|postfix" | xargs apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# Install Node.js and Yarn
RUN set -ex \
	&& curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
	&& add-apt-repository --yes "deb https://dl.yarnpkg.com/debian/ stable main" \
	&& apt-get install -y --no-install-recommends \
		yarn nodejs \
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

# Dashboard
COPY hack/entrypoints/dashboard-entrypoint.sh /

RUN set -ex \
	&& internalDirs=' \
		/src/src/dashboard/src/static \
		/src/src/dashboard/src/media \
	' \
	&& mkdir -p $internalDirs \
	&& chown -R archivematica:archivematica $internalDirs \
	&& yarn --cwd=/src/src/dashboard/frontend install --frozen-lockfile

WORKDIR /src/src/dashboard/src

USER archivematica

ENV DJANGO_SETTINGS_MODULE settings.local
ENV PYTHONPATH /src/src/dashboard/src/:/src/src/archivematicaCommon/lib/
ENV AM_GUNICORN_BIND 0.0.0.0:8000
ENV AM_GUNICORN_CHDIR /src/src/dashboard/src
ENV FORWARDED_ALLOW_IPS *

RUN set -ex \
	&& ./manage.py collectstatic --noinput --clear \
	&& ./manage.py compilemessages

ENV DJANGO_SETTINGS_MODULE settings.production

EXPOSE 8000

USER root

ENTRYPOINT ["sh", "/dashboard-entrypoint.sh"]