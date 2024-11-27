import uvicorn
from fastapi import FastAPI, Depends, HTTPException
import httpx
import json
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from keyclockclient import KeycloakClient, get_current_user
from typing import Dict

# Setup API Gateway
app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str


class OrderRequest(BaseModel):
    product_id: str
    quantity: int
    email: str


keycloak_client = KeycloakClient(
    server_url="http://keycloak:8080",
    realm_name="microservice-fastapi",               
    client_id="api-gateway",        
    client_secret="xJwOM4KX2VlvS1sEVUs6xgKYaE5CUBuo"  
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





@app.post("/login")
async def auth_login(request: LoginRequest): 
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth-service:8088/login", json=request.dict())
        print(response.json())
        return {"result": response.json()}

@app.get("/products")
async def get_products(token: str = Depends(oauth2_scheme)):
    userinfo = keycloak_client.verify_token(token)
    async with httpx.AsyncClient() as client:
        response = await client.get("http://product-service:8081/products", headers={"Authorization": f"Bearer {token}"})
        return response.json()

@app.post("/orders")
async def create_order(order: OrderRequest, token: str = Depends(oauth2_scheme)):
    print("token : {}".format(token))
    userinfo = keycloak_client.verify_token(token)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://order-service:8082/create_order", 
            json=order.model_dump(),
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084, reload=True)
