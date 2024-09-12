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
            # taken from https://stackoverflow.com/questions/8802860/checking-whether-a-string-starts-with-xxxx
            if (container.name.startswith("free-") and container.status == "running"):
                container.reload()
                state = container.attrs['State']
                start = state['FinishedAt']
                start_time = parse_timestamp(start)
                # taken from https://stackoverflow.com/questions/2591845/comparing-a-time-delta-in-python
                if (datetime.now(timezone.utc) - start_time > timedelta(minutes=1)):
                    print("stoping a container")
                    container.stop()
                    supabase.table("user_extra").update({"container_started": False, "container_used": True}).eq("container_code", container.name).execute()

checkContainers()