from fastapi import HTTPException, Header

async def get_token_header(internal_token:str = Header(...)):
    if internal_token != "allowed":
        raise HTTPException(status_code=400, detail="internal token header invalid")