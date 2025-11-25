import os
import subprocess
import sys

print("---------------------------------------------------")
print(" Air Quality Index – Full Stack App")
print(" Starting Backend + Frontend + Redis via Docker...")
print("---------------------------------------------------")

env_file = os.path.join("backend", ".env")

# Check for backend/.env
if not os.path.exists(env_file):
    print("ERROR: backend/.env file not found!")
    print("Create backend/.env with:")
    print("OPENWEATHER_API_KEY=your_api_key_here")
    sys.exit(1)

print("Loading environment variables from backend/.env")

# Load environment variables safely
with open(env_file) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" in line:
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

# Run docker compose
try:
    subprocess.run(["docker", "compose", "up", "--build"], check=True)
except FileNotFoundError:
    print("ERROR: Docker is not installed or not in PATH")
    sys.exit(1)
except subprocess.CalledProcessError:
    print("ERROR: Docker compose encountered an issue")
    sys.exit(1)
