import amqp from "amqplib";

class RabbitMQService {
  private connection: any = null;
  private channel: any = null;

  async connect(): Promise<void> {
    const rabbitUser = process.env.RABBITMQ_DEFAULT_USER || "guest";
    const rabbitPass = process.env.RABBITMQ_DEFAULT_PASS || "guest";
    const rabbitHost = process.env.RABBITMQ_HOST || "localhost";
    const rabbitPort = process.env.RABBITMQ_PORT || "5672";

    const url = `amqp://${rabbitUser}:${rabbitPass}@${rabbitHost}:${rabbitPort}`;

    try {
      console.log(`🐰 Connecting to RabbitMQ at ${rabbitHost}...`);

      this.connection = await amqp.connect(url);

      if (this.connection) {
        this.channel = await this.connection.createChannel();

        if (this.channel) {
          await this.channel.assertQueue("compliance_queue", { durable: true });
          console.log("✅ Connected to RabbitMQ successfully!");
        }
      }
    } catch (error) {
      console.error("❌ Error connecting to RabbitMQ:", error);
    }
  }

  async sendToQueue(data: any): Promise<boolean> {
    if (!this.channel) {
      console.error("❌ Channel not ready");
      return false;
    }

    const sent = this.channel.sendToQueue(
      "compliance_queue",
      Buffer.from(JSON.stringify(data)),
      { persistent: true }
    );

    return sent;
  }
}

export const rabbitMQ = new RabbitMQService();
