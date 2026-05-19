FROM quay.io/nandal_sanjeet/python:3.10

RUN pip3 install pymysql mcp httpx fastmcp && mkdir /opt/my-mcp-server

WORKDIR /opt/my-mcp-server

COPY server.py /opt/my-mcp-server

EXPOSE 8000

CMD ["python3", "server.py"] 
