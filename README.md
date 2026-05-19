# Install MCP Server and Mariadb Server manually
 
apt update
apt install -y openssh-server vim
apt install -y mariadb-server mariadb-client
apt install -y python3-pip
apt install -y python3-full python3-venv
mkdir /opt/my-mcp-server
systemctl start mariadb.service
systemctl status mariadb.service
mysql
mysqladmin password redhat
mysql -u root -p -h 127.0.0.1 -P 3306
systemctl enable mariadb.service
python3 -m venv /opt/my-mcp-server/venv
source /opt/my-mcp-server/venv/bin/activate
cd /opt/my-mcp-server/
ls
pip3 install mcp fastmcp
pip3 install httpx
pip3 install pymysql
python3 server.py 
