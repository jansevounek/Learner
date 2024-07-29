import docker
from supabase import create_client, Client
import os
import time
from datetime import datetime, timezone, timedelta

url = os.getenv("VITE_SUPABASE_URL")
key = os.getenv("VITE_SUPABASE_KEY")
supabase: Client = create_client(url, key)

client = docker.from_env()

def parse_timestamp(timestamp):

    if timestamp.endswith('Z'):
        timestamp = timestamp[:-1] + '+00:00'
    return datetime.fromisoformat(timestamp)

def checkContainers():
    begin = datetime.now(timezone.utc)
    print("Listening to all containers")
    while True:
        print("Uptime: " + str(datetime.now(timezone.utc) - begin))
        time.sleep(60)
        containers = client.containers.list(all=True)

        for container in containers:
            if (container.image.id == "sha256:e3bfc0ed8a671eae5b9e082413bbfe65feb157512a94285230397b541fc80f09" and container.status == "running"):
                container.reload()
                state = container.attrs['State']
                start = state['FinishedAt']
                start_time = parse_timestamp(start)
                # taken from https://stackoverflow.com/questions/2591845/comparing-a-time-delta-in-python
                if (datetime.now(timezone.utc) - start_time > timedelta(minutes=30)):
                    print("stoping a container")
                    container.stop()
                    supabase.table("user_extra").update({"container_started": False, "container_used": True}).eq("container_code", container.name).execute()

checkContainers()