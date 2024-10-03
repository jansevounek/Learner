import os
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

__all__ = ['supabase', 'getUserExtra', 'getUserContainers', 'getUserLimitations']