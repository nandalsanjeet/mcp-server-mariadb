"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py

Python code to connect to mariadb server and query for database

Install prerequisite
    pip install pymysql

"""

from fastmcp import FastMCP
import pymysql
from pymysql.err import OperationalError, InternalError


# Create an MCP server
mcp = FastMCP("My Server")

DB_CONFIG = {
    "host": "db_server",
    "port": 3306,
    "user": "root",
    "password": "",
    # do not set 'database' here because some operations (e.g., listing/creating/dropping DBs) do not require a default DB
    "connect_timeout": 5,
    "autocommit": True
}

def _get_connection(config=None):
    cfg = DB_CONFIG.copy()
    if config:
        cfg.update(config)
    return pymysql.connect(host=cfg["host"],
                           port=cfg.get("port", 3306),
                           user=cfg["user"],
                           password=cfg["password"],
                           connect_timeout=cfg.get("connect_timeout", 5),
                           autocommit=cfg.get("autocommit", True))

@mcp.tool()
def list_databases(config=None):
    """
    Connects to MariaDB and returns a list of database names.
    """
    conn = None
    try:
        conn = _get_connection(config)
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES;")
            rows = cur.fetchall()
            # rows are tuples like ('information_schema',)
            return [r[0] for r in rows]
    finally:
        if conn:
            conn.close()

@mcp.tool()
def create_database(db_name, config=None, if_not_exists=True, charset="utf8mb4", collate="utf8mb4_general_ci"):
    """
    Creates a database on the MariaDB server.
    - db_name: string (no surrounding backticks)
    - if_not_exists: adds IF NOT EXISTS clause to avoid error if DB exists
    - returns True if created or already exists, False on failure (raises on severe errors)
    """
    if not db_name or ";" in db_name or "`" in db_name:
        raise ValueError("Invalid database name")
    sql = f"CREATE DATABASE {'IF NOT EXISTS ' if if_not_exists else ''}`{db_name}` DEFAULT CHARACTER SET {charset} COLLATE {collate};"
    conn = None
    try:
        conn = _get_connection(config)
        with conn.cursor() as cur:
            cur.execute(sql)
        return True
    except (OperationalError, InternalError) as e:
        # re-raise or return False depending on desired behavior; here we re-raise for clarity
        raise
    finally:
        if conn:
            conn.close()

@mcp.tool()
def drop_database(db_name, config=None, if_exists=True):
    """
    Drops a database on the MariaDB server.
    - db_name: string (no surrounding backticks)
    - if_exists: adds IF EXISTS clause to avoid error if DB does not exist
    - returns True if dropped (or didn't exist when if_exists=True)
    """
    if not db_name or ";" in db_name or "`" in db_name:
        raise ValueError("Invalid database name")
    sql = f"DROP DATABASE {'IF EXISTS ' if if_exists else ''}`{db_name}`;"
    conn = None
    try:
        conn = _get_connection(config)
        with conn.cursor() as cur:
            cur.execute(sql)
        return True
    except (OperationalError, InternalError) as e:
        raise
    finally:
        if conn:
            conn.close()


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
