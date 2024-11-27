from keycloak import KeycloakOpenID
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer


class KeycloakClient:
    def __init__(self, server_url: str, realm_name: str, client_id: str, client_secret: str):
        self.keycloak_openid = KeycloakOpenID(
            server_url=server_url,
            realm_name=realm_name,
            client_id=client_id,
            client_secret_key=client_secret,
        )

    def verify_token(self, token: str):
        try:
            
            return self.keycloak_openid.decode_token(token)
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid token or expired")


