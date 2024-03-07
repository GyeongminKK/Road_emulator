import pika
def insert_tag_queue(msg, thread_id) :
    mq_ip = '127.0.0.1' 
    qname = 'RMQ_TAG_QNAME'
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_ip, port=5672, heartbeat=0))
        channel = connection.channel()
        channel.queue_declare(queue=qname, durable=True)
        channel.basic_publish(exchange='', routing_key=qname, body=msg)
        print(f"Thread #{thread_id} [{qname}] success")
        connection.close()
        return True
    except Exception as e:
        print('[RabbitMQ 상태 체크] ' + str(e))

__all__ = [
    'insert_tag_queue'
]