from fastapi import Header
from fastapi import HTTPException


async def get_token_header(x_auth_token: str = Header(default="")):
    # TODO: implement proper JWT token validation
    if not x_auth_token:
        raise HTTPException(status_code=403, detail="Not Authorized")
