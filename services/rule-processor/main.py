from fastapi import FastAPI
import pika
import json
import os
import threading
import time

app = FastAPI()

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
QUEUE_NAME = "compliance_queue"

def process_message(ch, method, properties, body):
    """
    Função Callback: Executada toda vez que chega uma mensagem.
    Aqui é onde aplicamos a "Lógica de Negócio" (Regras de Compliance).
    """
    try:
        data = json.loads(body)
        print(f" [x] Recebido: {data}")
                
        amount = data.get("amount", 0)
        transaction_id = data.get("transactionId", "UNKNOWN")

        if amount > 10000:
            status = "REPROVADO (Review Necessário)"
            color = "\033[91m" 
        else:
            status = "APROVADO"
            color = "\033[92m" 
        
        print(f"{color} [>>>] Processando TX {transaction_id} | Valor: {amount} | Status: {status} \033[0m")
        
        time.sleep(1) 

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f" [!] Erro ao processar mensagem: {e}")
        
def start_consumer():
    """
    Conecta ao RabbitMQ e inicia o loop de consumo.
    Inclui lógica de reconexão automática caso o RabbitMQ caia.
    """
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    
    while True:
        try:
            print(f" [*] Tentando conectar ao RabbitMQ em {RABBIT_HOST}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
            )
            channel = connection.channel()
            
            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

            print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
            channel.start_consuming()
        
        except pika.exceptions.AMQPConnectionError:
            print(" [!] Falha na conexão. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f" [!] Erro inesperado: {e}")
            time.sleep(5)

@app.on_event("startup")
def startup_event():
    
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "rule-processor"}