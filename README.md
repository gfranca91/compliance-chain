# ComplianceChain 🛡️

**ComplianceChain** is a proof-of-concept (PoC) platform designed to simulate a high-throughput financial compliance workflow. It demonstrates a **polyglot microservices architecture** where independent services communicate asynchronously to validate transaction data.

## 🏗 Architecture & Design Decisions

The system is built to decouple data ingestion from business rule processing, ensuring scalability and fault tolerance.

- **Asynchronous Communication:** Uses **RabbitMQ** as a message broker to buffer incoming requests, allowing the system to handle spikes in traffic without blocking the ingestion service.
- **Polyglot Stack:** Leverages the strengths of different ecosystems:
  - **Node.js (TypeScript):** Handles high I/O concurrency for the API Gateway/Ingestor.
  - **Python (FastAPI):** dedicated to data processing and complex rule evaluation (simulating data science/ML workloads).
- **Containerization:** Fully orchestrated with **Docker Compose** for a consistent development and deployment environment.

## 🚀 Tech Stack

- **Ingestion Service:** Node.js, Express, TypeScript
- **Processing Service:** Python 3, FastAPI
- **Message Broker:** RabbitMQ (AMQP)
- **Infrastructure:** Docker, Docker Compose

## 📦 How to Run

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/gfranca91/compliance-chain.git](https://github.com/gfranca91/compliance-chain.git)
    cd compliance-chain
    ```

2.  **Start the ecosystem:**

    ```bash
    docker-compose up --build
    ```

3.  **Test the Flow:**
    The API will be available at `http://localhost:3000`.

---

_Developed to demonstrate proficiency in Distributed Systems and Event-Driven Architecture._
