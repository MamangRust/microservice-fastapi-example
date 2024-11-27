import asyncio
import json
import smtplib
from aiokafka import AIOKafkaConsumer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from prometheus_client import start_http_server, Counter, Gauge
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Initialize OpenTelemetry Tracing
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({ SERVICE_NAME: "email-service"})
))
tracer = trace.get_tracer(__name__)

# Prometheus metrics
email_sent_counter = Counter('emails_sent', 'Total number of emails sent')
email_failed_counter = Counter('emails_failed', 'Total number of email failures')
email_latency_gauge = Gauge('email_send_latency', 'Latency of email sending process in seconds')

KAFKA_BROKER = "kafka:9092"

# Kafka consumer with OpenTelemetry instrumentation
AIOKafkaInstrumentor().instrument()

async def consume_email_events():
    consumer = AIOKafkaConsumer(
        "send-email",
        bootstrap_servers=KAFKA_BROKER,
        group_id="email_service",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            print(f"Received message from Kafka: {data}")
            email = data.get("email")
            message = data.get("message")

            if not email or not message:
                print("Error: Email or message is missing.")
                continue

            print(f"Sending email to {email}: {message}")

            # Tracing the email sending process
            with tracer.start_as_current_span("send_email"):
                # Measure the latency of sending the email
                email_latency_gauge.set(0)  # Resetting before the email is sent
                start_time = time.time()

                msg = MIMEMultipart()
                msg['From'] = "reba.schumm20@ethereal.email"
                msg['To'] = email
                msg['Subject'] = "Your Order Confirmation"

                body = MIMEText(message, 'plain')
                msg.attach(body)

                try:
                    # Send the email
                    with smtplib.SMTP("smtp.ethereal.email", 587) as server:
                        server.starttls()
                        server.login("reba.schumm20@ethereal.email", "6AgmyyMVAvsQTrGgCM")
                        server.sendmail("reba.schumm20@ethereal.email", email, msg.as_string())
                    
                    # Update Prometheus counters on success
                    email_sent_counter.inc()

                except Exception as e:
                    print(f"Failed to send email to {email}: {e}")
                    # Update Prometheus counters on failure
                    email_failed_counter.inc()

                # Record the latency
                email_latency_gauge.set(time.time() - start_time)

    finally:
        await consumer.stop()

async def main():
    start_http_server(8083)  
    await consume_email_events()

if __name__ == "__main__":
    import time
    asyncio.run(main())
