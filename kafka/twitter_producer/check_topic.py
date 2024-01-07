from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import time

time.sleep(15)

#Create topic, just run 1 time
kafka_admin_client = KafkaAdminClient(bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'])
topics = kafka_admin_client.list_topics()
if 'twitterData' not in topics:
    topic = NewTopic(name='twitterData', num_partitions=3, replication_factor=1)
    kafka_admin_client.create_topics(new_topics=[topic], validate_only=False)

time.sleep(10)
#Check topic
kafka_admin_client = KafkaAdminClient(bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'])
topics = kafka_admin_client.list_topics()
print("List of topics:")
for topic in topics:
    print(topic)
