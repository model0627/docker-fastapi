from datetime import datetime, timedelta
from typing import Annotated, Any, Literal

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader

from pydantic import BaseModel
from jose import ExpiredSignatureError, JWTError, jwt

API_TOKEN = "SECRET_API_TOKEN"
JWT_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# temp
# decode_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiRGluZXNoIn0.7Fwj-RvoEP2-LfB5q05pdTvMl7pFpoQgwXYq3EOLens"
decode_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiRGluZXNoIiwiZXhwaXJlIjoiMjAyNC0wNC0xOCAwNDo1MDowNiJ9.o9vvz5xPmjkpPvZ4fluX42DejP6qcsIO9Lfu7un6Ccc"
encode_token = {"name": "Dinesh"}

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class Role(BaseModel):
    """The role of the session.

    Params
    ------
    type : Literal["user", "service"]
        The type of role.
    user_id : str | None
        The user's JWT 'sub' claim, or the service's user_id.
        This can be None for internal services, or when a user hasn't been set for the role.
    service_id : str | None = None
        The service's role name, or None if the role is a user.


    User roles
    ----------
    - User roles are authenticated via JWT.
    - The `user_id` is the user's JWT 'sub' claim.
    - User roles do not have an associated `service_id`, this must be None.

    Service roles
    -------------
    - Service roles are authenticated via API key.
    - Used for internal services to authenticate with the API.
    - A service's `user_id` is the user it's acting on behalf of. This can be None for internal services.
    """

    type: Literal["user", "service"]
    user_id: str | None = None
    service_id: str | None = None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, API_TOKEN, ALGORITHM)

    return encoded_jwt


@app.get("jwt/encode")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    encoded_data = jwt.encode(encode_token,
                              key=JWT_KEY,
                              algorithm=ALGORITHM)

    payload = create_access_token(encode_token)
    print(payload)
    return encoded_data

@app.get("jwt/decode")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    payload = jwt.decode(
        decode_token,
        key=JWT_KEY,
        algorithms=ALGORITHM,
        # NOTE: Workaround, not sure if there are alternatives
        options={"verify_aud": False},
    )
    user_id: str = payload.get("sub")

    return payload



@app.get("oauth/encode")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    encoded_data = create_access_token(encode_token)

    return encoded_data


@app.get("oauth/login")
async def protected_route(token: Annotated[str, Depends(oauth2_scheme)]):
    

    raise CREDENTIALS_EXCEPTION