#!/bin/bash
useradd -d /home/sshonly -g sshonly -s /sbin/nologin $1
echo $1:$2 |chpasswd
