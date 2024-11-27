import uvicorn
import json
import asyncio
from typing import Dict
from fastapi import FastAPI, Depends, Security
from fastapi.responses import JSONResponse, Response
from aiokafka import AIOKafkaConsumer
from keyclockclient import KeycloakClient
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from fastapi.security import OAuth2PasswordBearer
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from prometheus_client import Counter, Gauge, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Products dictionary
products = {"product1": {"quantity": 10}, "product2": {"quantity": 5}}

KAFKA_BROKER = "kafka:9092"

# Initialize Keycloak client
keycloak_client = KeycloakClient(
    server_url="http://keycloak:8080",
    realm_name="microservice-fastapi",
    client_id="product-service",
    client_secret="KnT6H4IAb1scwUQgpG5CjHIoGvdhLQ2K"
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_user(token: str = Security(oauth2_scheme)):
    return keycloak_client.verify_token(token)

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({ "service.name": "product-service" })
))
tracer = trace.get_tracer(__name__)

# Configure OTLP Span Exporter
span_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Custom CollectorRegistry for Prometheus metrics
custom_registry = CollectorRegistry()

# Prometheus metrics
product_update_counter = Counter(
    'product_updates_received',
    'Total number of product update messages received',
    registry=custom_registry,
)

quantity_updated_gauge = Gauge(
    'product_quantity',
    'Current quantity of the product',

    registry=custom_registry
)

# Kafka instrumentation with OpenTelemetry
AIOKafkaInstrumentor().instrument()

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(custom_registry), media_type=CONTENT_TYPE_LATEST)


# Get all products
@app.get("/products")
async def get_products(current_user: Dict = Depends(get_current_user)):
    # Start tracing for the get_products request
    with tracer.start_as_current_span("get_products"):
        return {"message": "Here are your products", "product": products}

# Kafka consumer to listen to product updates
async def consume_product_updates():
    consumer = AIOKafkaConsumer(
        "product-updates",
        bootstrap_servers=KAFKA_BROKER,
        group_id="product_service",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            product_id = data["product_id"]
            quantity = data["quantity"]

            # Start a tracing span for processing product update
            with tracer.start_as_current_span(f"process_product_update_{product_id}"):
                if product_id in products:
                    products[product_id]["quantity"] -= quantity
                    print(f"Updated {product_id}: {products[product_id]}")

                    # Track the number of product updates
                    product_update_counter.inc()

                    # Update the current product quantity in Prometheus
                    quantity_updated_gauge.labels(product_id=product_id).set(products[product_id]["quantity"])

    finally:
        await consumer.stop()

# Start consumer on service startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_product_updates())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
