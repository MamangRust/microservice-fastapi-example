import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from keyclockclient import KeycloakClient, get_current_user
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from opentelemetry import metrics, trace

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from prometheus_client import Counter, Gauge, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

# OpenTelemetry Trace Configuration
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "auth-service"})
    )
)
tracer = trace.get_tracer(__name__)

span_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)




custom_registry = CollectorRegistry()


# Prometheus Counter
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests', registry=custom_registry)


app = FastAPI()


# OAuth2 password bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Keycloak Client Setup
keycloak_client = KeycloakClient(
    server_url="http://keycloak:8080",
    realm_name="microservice-fastapi",
    client_id="auth-service",
    client_secret="CQA1qheenTEY4syd9rCtUf6NpkL4456a",
)

class LoginRequest(BaseModel):
    username: str
    password: str

# Expose Prometheus Metrics on /metrics
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(custom_registry), media_type=CONTENT_TYPE_LATEST)


@app.post("/login")
async def login(request: LoginRequest):
    try:
        username = request.username
        password = request.password

        # Creating span for login operation
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("login"):
            token = keycloak_client.token(username, password)
        
        return {
            "access_token": token["access_token"],
            "verify_token": token["refresh_token"],
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/logout")
async def logout():
    return {"message": "Logout successful"}

@app.get("/verify_token")
async def verify_token(current_user: Dict = Depends(get_current_user)):
    try:
        return {"user_info": current_user}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
