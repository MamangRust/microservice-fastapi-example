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
            
            return self.keycloak_openid.decode_token(token, verify=True)
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid token or expired")

    def token(self, username: str, password: str):
        """Function to handle login and return access and refresh tokens."""
        try:
            # Fetch token using Keycloak's token endpoint
            token_response = self.keycloak_openid.token(
                username=username,
                password=password,
                grant_type="password",
            )
            return token_response  # This should return access_token, refresh_token, etc.
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error during login: {str(e)}")



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_user(token: str = Security(oauth2_scheme)):
    return KeycloakClient.verify_token(token)
