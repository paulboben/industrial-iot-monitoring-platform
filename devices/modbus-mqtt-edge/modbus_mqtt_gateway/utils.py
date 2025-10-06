import json

def format_payload(coils):
    """Convert coil list to JSON payload."""
    return json.dumps({"coils": coils})