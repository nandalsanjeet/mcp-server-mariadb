# mcp-server-mariadb

# Install MCP Server and Mariadb Server manually
 
   78  apt update
   79  apt install -y openssh-server vim
   84  apt install -y mariadb-server mariadb-client

   85  df -h
   86  cfdisk /dev/vda
   87  udevadm settle 
   88  lsblk 
   90  mkfs.ext4 /dev/vda4

  120  apt install -y python3-pip
  122  apt install -y python3-full python3-venv
  124  mkdir /opt/my-mcp-server

  160  systemctl start mariadb.service
  161  systemctl status mariadb.service
  164  mysql
  167  mysqladmin password redhat
  168  mysql -u root -p -h 127.0.0.1 -P 3306
  179  systemctl enable mariadb.service

  204  python3 -m venv /opt/my-mcp-server/venv
  205  source /opt/my-mcp-server/venv/bin/activate
  206  cd /opt/my-mcp-server/
  207  ls
  208  pip3 install mcp fastmcp
  209  pip3 install httpx

  214  pip3 install pymysql
  215  python3 server.py 
