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
    if user_id:
        try:
            response = supabase.table("user").select("*").eq("user_id", user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("user").select("*").eq("id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id or extra info id not provided - failed to fetch user extra")
    
# gets all of users containers
def getUserContainers(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    name = kwargs.get("name")
    id = kwargs.get("id")
    if id:
        try:
            response = supabase.table("container").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    elif user_id:
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            response = supabase.table("container").select("*").eq("extra_id", i).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("container").select("*").eq("extra_id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    elif name:
        try:
            response = supabase.table("container").select("*").eq("name", name).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id, extra_id, name or id not provided - failed to fetch users containers")

# gets user limitations
def getUserLimitations(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    id = kwargs.get("id")

    if id:
        try:
            response = supabase.table("limitations").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users limitations): {e}")
            return "Error occured", 500
    elif user_id:
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            response = supabase.table("limitations").select("*").eq("extra_id", i).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users limitations): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("limitations").select("*").eq("extra_id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users limitations): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id, extra_id, name or id not provided - failed to fetch users limitations")
    
# gets the container that is to be deleted
def getContainerByIdName(name, extra_id):
    try:
        response = supabase.table("container").select("*").eq("name", name).eq("extra_id", extra_id).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting users containers): {e}")
        return "Error occured", 500
    
def getTeam(**kwargs):
    id = kwargs.get("id")
    name = kwargs.get("name")
    code = kwargs.get("code")

    if id:
        try:
            response = supabase.table("team").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting team by id): {e}")
            return "Error occured", 500
    elif name:
        try:
            response = supabase.table("team").select("*").eq("name", name).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting team by name): {e}")
            return "Error occured", 500
    elif code:
        try:
            if (is_uuid(code)):
                response = supabase.table("team").select("*").eq("team_code", code).execute()
                return response.data
            else:
                return []
        except Exception as e:
            print(f"Error during Supabase query (during getting team by code): {e}")
            return "Error occured", 500
    else:
        raise ValueError("name or id not provided - failed to fetch team")

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

    if id:
        try:
            response = supabase.table("lesson").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting lesson by id): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("lesson").select("*").eq("creator_id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting lesson by extra_id): {e}")
            return "Error occured", 500
    elif name:
        try:
            response = supabase.table("lesson").select("*").eq("name", name).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting lesson by name): {e}")
            return "Error occured", 500
    elif user_id:
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            response = supabase.table("lesson").select("*").eq("creator_id", i).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting lesson by user_id): {e}")
            return "Error occured", 500
    elif team_id:
        try:
            response = supabase.table("lesson").select("*").eq("team_id", team_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting lesson by name): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id, extra_id or id not provided - failed to fetch lesson")


__all__ = ['supabase', 'getUserExtra', 'getUserContainers', 'getUserLimitations', 'getToBeDeletedContainer']