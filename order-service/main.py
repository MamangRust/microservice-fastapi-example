import uvicorn
import json
import asyncio
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from aiokafka import AIOKafkaProducer
from keyclockclient import KeycloakClient, get_current_user
from pydantic import BaseModel
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import Counter, Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

# FastAPI application and Kafka configuration
app = FastAPI()

KAFKA_BROKER = "kafka:9092"
producer = None

# Initialize Keycloak client
keycloak_client = KeycloakClient(
   server_url="http://keycloak:8080",
    realm_name="microservice-fastapi",               
    client_id="order-service",        
    client_secret="vASJSVIrVfwnprDwKZZn8hbRFADiiqFV"  
)

# OrderRequest model
class OrderRequest(BaseModel):
    product_id: str
    quantity: int
    email: str

# OpenTelemetry initialization
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "order-service"})
    )
)
tracer = trace.get_tracer(__name__)

# Configure OTLP Span Exporter
span_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Prometheus custom registry and metrics
custom_registry = CollectorRegistry()
order_created_counter = Counter(
    'orders_created', 
    'Total number of orders created', 
    registry=custom_registry
)
email_sent_counter = Counter(
    'emails_sent', 
    'Total number of emails sent', 
    registry=custom_registry
)
email_latency_gauge = Gauge(
    'email_send_latency', 
    'Latency of email sending process in seconds', 
    registry=custom_registry
)

# Startup and Shutdown events
@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    global producer
    if producer:
        await producer.stop()

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(custom_registry), media_type=CONTENT_TYPE_LATEST)


# Create order endpoint
@app.post("/create_order")
async def create_order(request: OrderRequest):
    # Start tracing for the create_order request
    with tracer.start_as_current_span("create_order"):
        product_event = {
            "product_id": request.product_id, 
            "quantity": request.quantity
        }
        # Send product update event
        await producer.send_and_wait("product-updates", json.dumps(product_event).encode("utf-8"))
        
        email_event = {
            "email": request.email, 
            "message": f"Your order for {request.product_id} has been created!"
        }

        # Track email send latency and send email event
        start_time = time.time()
        await producer.send_and_wait("send-email", json.dumps(email_event).encode("utf-8"))
        email_latency_gauge.set(time.time() - start_time)  # Record latency

        # Increment counters for metrics
        order_created_counter.inc()
        email_sent_counter.inc()

    return {"status": "Order created successfully"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8082, reload=True)
