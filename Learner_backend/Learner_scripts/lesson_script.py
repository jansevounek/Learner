import os
from time import sleep
from supabase import create_client, Client
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import docker

client = docker.from_env()

url: str = os.environ.get("VITE_SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_KEY")
supabase: Client = create_client(url, key)

def main():
    print("Lesson script running TODO - rework this")

    while True:
        sleep(1)
        lessons = supabase.table("lesson").select("*").execute().data

        currentDateTime = datetime.now()

        for lesson in lessons:
            end = lesson.get("end_time")
            endTime = datetime.fromisoformat(end.replace('Z', '+00:00'))
            if (currentDateTime - endTime) > timedelta(days=30):
                deleteTable(lesson)

def deleteTable(lesson):
    try:
        print("deleted lesson id: " + str(lesson.get("id")))
        supabase.table("lesson").delete().eq("id", lesson.get("id")).execute()
    except Exception as e:
        print("There was a problem during removal of the lesson: " + {e})
        return
    
    try:
        limit = supabase.table("limitations").select("*").eq("extra_id", lesson.get("creator_id")).execute().data
        lessons = limit[0].get("lessons")
        number = lessons - 1
        supabase.table("limitations").update({"lessons": number}).eq("extra_id", lesson.get("creator_id")).execute()
    except Exception as e:
        print("There was a problem during changing limits: " + str(e))
        return
    
    deleteContainers(lesson.get("name"))

def deleteContainers(name):
    try:
        containers = client.containers.list(all=True)

        for container in containers:
            if container.name.startswith(name + "-"):
                if container.status == "running":
                    container.stop()
                container.remove()
                
    except Exception as e:
        print(f"Error during deleting containers - lesson cancel: {e}")
        return "Error occured", 500

if __name__ == "__main__":
    main()