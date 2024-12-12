# Monolith E-commerce Project - README

## Overview
This project is a monolithic e-commerce application that integrates multiple service using **FastAPI** and **SQLAlchemy**. It leverages **PostgreSQL** as the database, and the architecture is containerized with **Docker Compose** for seamless setup and scaling. The system includes key components such as authentication, order processing, and product management, with observability tools for monitoring and debugging.

## Features
- **Authentication**: Login and verify tokens using Keycloak.
- **Product Management**: Get all products.
- **Order Management**: Create Order and send emails to the customer to apache kafka
- **Email Notifications**: Asynchronous email sending for transactional updates.
- **API Gateway**: A centralized entry point for all services.
- **Observability**: Integrated tools like Prometheus, Grafana, Jaeger, and OpenTelemetry.

---

## Tech Stack
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Message Broker**: Kafka
- **Monitoring and Observability**: Prometheus, Grafana, OpenTelemetry, Jaeger
- **Authentication**: Keycloak
- **Containerization**: Docker Compose

---

## Installation
```bash
# Clone the repository
$ git clone https://github.com/MamangRust/monolith-ecommerce-example.git
$ cd monolith-ecommerce

# Start the application
$ docker-compose up --build
```

### Access Services
- **API Gateway**: [http://localhost:8084](http://localhost:8084)
- **Keycloak**: [http://localhost:8080](http://localhost:8080)
- **Grafana**: [http://localhost:3000](http://localhost:3000)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Jaeger**: [http://localhost:16686](http://localhost:16686)

---

## Services Breakdown

### Authentication Service
- **Path**: `./auth-service`
- **Description**: Manages user authentication and roles using Keycloak.
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Port**: `8088`

### Product Service
- **Path**: `./product-service`
- **Description**: Get all products.
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Port**: `8081`

### Order Service
- **Path**: `./order-service`
- **Description**: Create Order and send emails to the customer to apache kafka
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Port**: `8082`

### Email Service
- **Path**: `./email-service`
- **Description**: Sends emails to the customer to apache kafka
- **Dependencies**: Kafka for message queueing.
- **Port**: `8083`

---

## Observability and Monitoring
- **Prometheus**: Collects metrics from all services and Kafka.
- **Grafana**: Visualizes collected metrics with dashboards.
- **Jaeger**: Traces requests across services for debugging.
- **OpenTelemetry**: Ensures consistent telemetry data across services.

---

## Visualizations
### Jaeger UI in grafana
![Jaeger](./images/jaeger.png)

### Prometheus in grafana

![Prometheus](./images/promethus.png)









```sh

curl -X GET "http://0.0.0.0:8084/products" \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMQ0lFQms3Nmd1S2duRHA5ZWJEaExRei1xZWdqdy1VYk9JbjJLdWUwekQwIn0.eyJleHAiOjE3MzI3MTk5ODUsImlhdCI6MTczMjcxOTY4NSwianRpIjoiZTk4NTI0YmMtM2JkOS00OTJmLTgyOGEtMzU2MzMzY2RkMjZlIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL21pY3Jvc2VydmljZS1mYXN0YXBpIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImU5YjI2ZThkLTUxNjMtNGQwZS1hNWEwLTkyYzllMzhjYjQyMSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImF1dGgtc2VydmljZSIsInNpZCI6IjQ3MzZlYjE5LTJiNGYtNGM4Ny05NDBkLTJlYjNiZDVkZjc2MSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2F1dGgtc2VydmljZTo4MDg4Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1pY3Jvc2VydmljZS1mYXN0YXBpIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJteSB1c2VyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibXl1c2VyIiwiZ2l2ZW5fbmFtZSI6Im15IiwiZmFtaWx5X25hbWUiOiJ1c2VyIiwiZW1haWwiOiJteXVzZXJAZ21haWwuY29tIn0.d1zIQqU_lIgvIX2cIEyPtcWPOQ-Fv46MAgwAzzwqEy__dLxO3ZHHtQZkgSaoGQkG1nZq4qXF_vLoEXLrIB71xZN69yCi5j5QX_nM6NmVtI8IKwYdWwVEktqlXupCp4DW-pqThlCGeNbrpHqr_42HpE7ewU5CMON4n4Yl_NbRcN2P6fwNeV-2xsNMKtCEJ46MQD0B9VyZFvnuog_SjSZqxXjk9EAZXcB3R2aECS_1CD-l_IprxPtMBjKk3zpIVlph8Anbl_X-4EcmtUfVHaGH8kSovVvNJpvPQ5oOpNZFXd2JqIPK4rfJIvvAYPSsV-E5TcMzZJCzU_GGHvKDoQ53yw"
```


```sh
curl -X POST "http://0.0.0.0:8084/orders" \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMQ0lFQms3Nmd1S2duRHA5ZWJEaExRei1xZWdqdy1VYk9JbjJLdWUwekQwIn0.eyJleHAiOjE3MzI3MTk5ODUsImlhdCI6MTczMjcxOTY4NSwianRpIjoiZTk4NTI0YmMtM2JkOS00OTJmLTgyOGEtMzU2MzMzY2RkMjZlIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL21pY3Jvc2VydmljZS1mYXN0YXBpIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImU5YjI2ZThkLTUxNjMtNGQwZS1hNWEwLTkyYzllMzhjYjQyMSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImF1dGgtc2VydmljZSIsInNpZCI6IjQ3MzZlYjE5LTJiNGYtNGM4Ny05NDBkLTJlYjNiZDVkZjc2MSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2F1dGgtc2VydmljZTo4MDg4Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1pY3Jvc2VydmljZS1mYXN0YXBpIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJteSB1c2VyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibXl1c2VyIiwiZ2l2ZW5fbmFtZSI6Im15IiwiZmFtaWx5X25hbWUiOiJ1c2VyIiwiZW1haWwiOiJteXVzZXJAZ21haWwuY29tIn0.d1zIQqU_lIgvIX2cIEyPtcWPOQ-Fv46MAgwAzzwqEy__dLxO3ZHHtQZkgSaoGQkG1nZq4qXF_vLoEXLrIB71xZN69yCi5j5QX_nM6NmVtI8IKwYdWwVEktqlXupCp4DW-pqThlCGeNbrpHqr_42HpE7ewU5CMON4n4Yl_NbRcN2P6fwNeV-2xsNMKtCEJ46MQD0B9VyZFvnuog_SjSZqxXjk9EAZXcB3R2aECS_1CD-l_IprxPtMBjKk3zpIVlph8Anbl_X-4EcmtUfVHaGH8kSovVvNJpvPQ5oOpNZFXd2JqIPK4rfJIvvAYPSsV-E5TcMzZJCzU_GGHvKDoQ53yw" \
-H "Content-Type: application/json" \
-d '{
    "product_id": "12345",
    "quantity": 2,
    "email": "user@example.com"
}'
```
