import sys
import huggingface_hub

if len(sys.argv) < 2:
    raise ValueError("Usage: python import.py <HUGGINGFACE_TOKEN>")

token = sys.argv[1]
huggingface_hub.login(token=token, new_session=False, add_to_git_credential=True)
