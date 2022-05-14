from fastapi import Header, HTTPException


# TODO: implement proper JWT token validation


async def get_token_header(x_auth_token: str = Header(default="")):
    pass
    # if not x_auth_token:
    #     raise HTTPException(status_code=403, detail="Not Authorized")
