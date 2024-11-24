import os
import base64
import hashlib
import secrets

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode("utf-8").rstrip("=")
    
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")
    
    state = secrets.token_urlsafe(16)

    return {
        "code_challenge": code_challenge,
        "state": state,
    }
