#!/bin/sh

mkdir -p /var/archivematica/sharedDirectory
chown -R archivematica:archivematica /var/archivematica/sharedDirectory

su archivematica

su archivematica --command "python /src/src/MCPClient/lib/archivematicaClient.py" 
