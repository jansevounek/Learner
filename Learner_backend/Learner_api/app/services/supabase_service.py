import os
import uuid
from supabase import create_client, Client

url: str = os.environ.get("VITE_SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_KEY")
supabase: Client = create_client(url, key)

# gets users extra information
# one of extra_id or user_id is mandatory
def getUserExtra(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    code = kwargs.get("code")

    querry_field = ""
    querry_value = ""

    if (extra_id):
        querry_field = "id"
        querry_value = extra_id
    elif (user_id):
        querry_field = "user_id"
        querry_value = user_id
    elif (code):
        querry_field = "user_code"
        querry_value = code
    else:
        raise ValueError("user_id or extra info id not provided - failed to fetch user extra")
    
    try:
        response = supabase.table("user").select("*").eq(querry_field, querry_value).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting user extra): {e}")
        return "Error occured", 500
    
# gets user limitations
def getUserLimitations(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    id = kwargs.get("id")

    querry_field = ""
    querry_value = ""

    if (extra_id):
        querry_field = "extra_id"
        querry_value = extra_id
    elif (user_id):
        querry_field = "extra_id"
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            querry_value = i
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    elif (id):
        querry_field = "id"
        querry_value = id
    else:
        raise ValueError("user_id, extra_id or id not provided - failed to fetch users limitations")
    
    try:
        response = supabase.table("limitations").select("*").eq(querry_field, querry_value).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting limitations): {e}")
        return "Error occured", 500
    
def getTeam(**kwargs):
    id = kwargs.get("id")
    name = kwargs.get("name")
    code = kwargs.get("code")

    querry_field = ""
    querry_value = ""

    if (name):
        querry_field = "name"
        querry_value = name
    elif (code):
        if (is_uuid(code)):
            querry_field = "team_code"
            querry_value = code
        else:
            return []
    elif (id):
        querry_field = "id"
        querry_value = id
    else:
        raise ValueError("name, id or team_code not provided - failed to fetch team")
    
    try:
        response = supabase.table("team").select("*").eq(querry_field, querry_value).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting team): {e}")
        return "Error occured", 500

# taken from https://stackoverflow.com/questions/53847404/how-to-check-uuid-validity-in-python
def is_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
    
def getLesson(**kwargs):
    id = kwargs.get("id")
    user_id = kwargs.get("user_id")
    extra_id = kwargs.get("extra_id")
    name = kwargs.get("name")
    team_id = kwargs.get("team_id")

    querry_field = ""
    querry_value = ""

    if (extra_id):
        querry_field = "extra_id"
        querry_value = extra_id
    elif (user_id):
        querry_field = "creator_id"
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            querry_value = i
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    elif (id):
        querry_field = "id"
        querry_value = id
    elif (name):
        querry_field = "name"
        querry_value = name
    elif (team_id):
        querry_field = "team_id"
        querry_value = team_id
    else:
        raise ValueError("user_id, extra_id or id not provided - failed to fetch lesson")
    
    try:
        response = supabase.table("lesson").select("*").eq(querry_field, querry_value).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting lesson): {e}")
        return "Error occured", 500
    
def getContainer(**kwargs):
    id = kwargs.get("id")
    extra_id = kwargs.get("extra_id")
    lesson_id = kwargs.get("lesson_id")
    name = kwargs.get("name")

    if id:
        try:
            response = supabase.table("container").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting container by id): {e}")
            return "Error occured", 500
    elif extra_id and lesson_id:
        try:
            response = supabase.table("container").select("*").eq("user_id", extra_id).eq("lesson_id", lesson_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting container by extra_id): {e}")
            return "Error occured", 500
    elif name:
        try:
            response = supabase.table("container").select("*").eq("name", name).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting container by name): {e}")
            return "Error occured", 500
    else:
        raise ValueError("(lesson_id and extra_id) or id not provided - failed to fetch container")
    
def getScript(**kwargs):
    id = kwargs.get("id")
    container_id = kwargs.get("container_id")
    container_name = kwargs.get("container_name")

    if id:
        try:
            response = supabase.table("container_script").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting script by id): {e}")
            return "Error occured", 500
    elif container_id:
        try:
            response = supabase.table("container_script").select("*").eq("container_id", container_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting script by container_id): {e}")
            return "Error occured", 500
    elif container_name:
        try:
            response = supabase.table("container_script").select("*").eq("container_name", container_name).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting script by container_id): {e}")
            return "Error occured", 500
    else:
        raise ValueError("container_id or id not provided - failed to fetch script")


__all__ = ['supabase', 'getUserExtra', 'getUserLimitations', 'getToBeDeletedContainer']