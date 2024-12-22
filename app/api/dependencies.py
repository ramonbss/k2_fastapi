from fastapi import HTTPException, Header


async def validate_token(authorization_token: str = Header(...)):
    """validate and use the token for protected routes"""
    if not authorization_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    return authorization_token
