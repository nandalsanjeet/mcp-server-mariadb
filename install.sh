#!/bin/bash

docker pull quay.io/nandal_sanjeet/mariadb-server:latest
docker pull quay.io/nandal_sanjeet/mcp-server-mariadb:latest

docker network create db_net
docker run -d --name db_server --network db_net quay.io/nandal_sanjeet/mariadb-server:latest
docker run -d --name mcp-server-mariadb -p 8000:8000 --net db_net quay.io/nandal_sanjeet/mcp-server-mariadb:latest

apt install -y npm
npm install @modelcontxtprotocol/inspector

echo "[db_server] - Mariadb Server (container) is ready up and running"
echo ""
echo "[mcp-server-maridb] - MCP Server Mariadb Servr (container) is ready up and running. The Server is exposed to (8000) port with the host machine"
echo ""
echo "MCP Inspector is ready"
