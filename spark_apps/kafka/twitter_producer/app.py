from producer import TwitterProducer
from kafka import KafkaAdminClient
from kafka.admin import NewTopic

def run_service():
    # # Create topic, just run 1 time
    # kafka_admin_client = KafkaAdminClient(bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'])
    # topics = kafka_admin_client.list_topics()
    # if 'twitterData' not in topics:
    #     topic = NewTopic(name='twitterData', num_partitions=3, replication_factor=1)
    #     kafka_admin_client.create_topics(new_topics=[topic], validate_only=False)

    producer = TwitterProducer()
    print(f"After create producer")
    producer.run()

if __name__ == "__main__":
    print("------Start----- ")
    run_service()