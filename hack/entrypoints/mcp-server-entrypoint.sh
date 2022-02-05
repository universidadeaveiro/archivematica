#!/bin/sh

mkdir -p /var/dip-uploads
mkdir -p /var/archivematica/sharedDirectory

chown -R archivematica:archivematica /var/dip-uploads
chown -R archivematica:archivematica /var/archivematica/sharedDirectory

su archivematica

su archivematica --command "python /src/src/MCPServer/lib/archivematicaMCP.py"
