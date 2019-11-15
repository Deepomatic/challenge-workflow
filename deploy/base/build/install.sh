#!/bin/bash

set -e

apt-get update

# Install base dependencies
apt-get install -y --no-install-recommends \
        locales cmake pkg-config \
        build-essential autoconf libtool\
        libffi-dev libssl-dev libpq-dev \
        curl wget unzip \
        ca-certificates python3-dev python3-pip \
        python3-setuptools python3-wheel \
        git

    # UTF8
locale-gen en_US.UTF-8

pip3 install -r $(dirname $0)/requirements.txt --no-cache-dir


rm -rf /var/lib/apt/lists/* || :
