import express, { Request, Response } from "express";
import dotenv from "dotenv";
import { rabbitMQ } from "./rabbitmq";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/health", (req: Request, res: Response) => {
  res.json({ status: "OK", service: "data-ingestor" });
});

app.post("/ingest", async (req: Request, res: Response) => {
  const data = req.body;

  if (!data || !data.transactionId || !data.amount) {
    return res
      .status(400)
      .json({
        error: "Invalid payload. transactionId and amount are required.",
      });
  }

  const success = await rabbitMQ.sendToQueue(data);

  if (success) {
    console.log(`📤 Message sent: ${data.transactionId}`);
    return res
      .status(202)
      .json({
        status: "queued",
        message: "Transaction received for processing",
      });
  } else {
    return res.status(500).json({ error: "Failed to queue message" });
  }
});

const startServer = async () => {
  await rabbitMQ.connect();

  app.listen(PORT, () => {
    console.log(`🚀 Data Ingestor running on port ${PORT}`);
  });
};

startServer();
