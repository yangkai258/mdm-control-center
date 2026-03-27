#!/bin/sh
cp /tmp/mdm-server /app/mdm-server
chmod +x /app/mdm-server
exec /app/mdm-server
