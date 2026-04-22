import socket
import time
import os

def tcp_ping(host, port, timeout=5):
    """
    Attempts a TCP connection to simulate a ping. 
    Returns (Success, Message)
    """
    try:
        start = time.time()
        # Create a connection to the specific DB port
        with socket.create_connection((host, port), timeout=timeout):
            duration = (time.time() - start) * 1000
            return True, f"SUCCESS: Reachable in {duration:.2f}ms"
    except socket.timeout:
        return False, "ERROR: Connection timed out (check Security Groups/NACLs)"
    except ConnectionRefusedError:
        return False, "ERROR: Connection refused (DB is down or port is wrong)"
    except Exception as e:
        return False, f"ERROR: {str(e)}"

# --- CONFIGURATION ---
# Use your RDS Private Endpoint and Port
RDS_HOST =os.environ.get("DB_HOST", "ht-workflow.c9hukjucdlzt.us-east-1.rds.amazonaws.com")
RDS_PORT = 5432  # 5432 for Postgres, 3306 for MySQL/Aurora

if __name__ == "__main__":
    print(f"Testing connectivity to {RDS_HOST} on port {RDS_PORT}...")
    success, message = tcp_ping(RDS_HOST, RDS_PORT)
    print(message)
