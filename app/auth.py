
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security=HTTPBasic()

def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    if creds.username == "admin" and creds.password == "admin":
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")
