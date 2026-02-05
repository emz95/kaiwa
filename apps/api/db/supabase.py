import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Calculate path to root .env file
# From: apps/api/db/supabase.py
# To: root/.env
env_path = Path(__file__).parent.parent.parent.parent / ".env"

# Debug: Print the path we're looking for
print(f"DEBUG: Looking for .env at: {env_path}")
print(f"DEBUG: File exists: {env_path.exists()}")
print(f"DEBUG: Absolute path: {env_path.resolve()}")

# Try to load the .env file - convert Path to string
loaded = load_dotenv(str(env_path), override=True)
print(f"DEBUG: First load attempt: {loaded}")

# If file exists but wasn't loaded, try without override
if env_path.exists() and not loaded:
    loaded = load_dotenv(str(env_path), override=False)
    print(f"DEBUG: Second load attempt: {loaded}")

# Also try loading from current directory as fallback
if not loaded:
    print("DEBUG: Trying fallback load from current directory")
    load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    # Debug: Check what's actually in the file
    env_vars_in_file = []
    raw_file_content = []
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                lines = f.readlines()
                raw_file_content = [line.rstrip() for line in lines]  # Keep all lines including empty
                env_vars_in_file = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
        except Exception as e:
            env_vars_in_file = [f"Error reading file: {e}"]
            raw_file_content = [f"Error: {e}"]
    
    error_msg = (
        f"Missing Supabase credentials in environment variables.\n"
        f"Looking for .env at: {env_path}\n"
        f"File exists: {env_path.exists()}\n"
        f"File loaded: {loaded}\n"
        f"Raw file content (first 10 lines): {raw_file_content[:10]}\n"
        f"Valid variables found: {env_vars_in_file[:5]}\n"
        f"File size: {env_path.stat().st_size if env_path.exists() else 0} bytes\n"
        f"NEXT_PUBLIC_SUPABASE_URL: {'SET' if SUPABASE_URL else 'NOT SET'}\n"
        f"SUPABASE_SERVICE_ROLE_KEY: {'SET' if SUPABASE_SERVICE_ROLE_KEY else 'NOT SET'}\n"
        "Required variables: NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY\n"
        "Make sure your .env file has these exact variable names (no spaces around =)"
    )
    raise ValueError(error_msg)

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)