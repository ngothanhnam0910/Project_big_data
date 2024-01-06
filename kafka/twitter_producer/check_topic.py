from kafka import KafkaAdminClient
from kafka.admin import NewTopic

# #Create topic, just run 1 time
# kafka_admin_client = KafkaAdminClient(bootstrap_servers=['127.0.0.1:9092','127.0.0.1:9093','127.0.0.1:9094'])
#
# topic = NewTopic(name='twitterData', num_partitions=3, replication_factor=1)
# kafka_admin_client.create_topics(new_topics=[topic], validate_only=False)

#Check topic
kafka_admin_client = KafkaAdminClient(bootstrap_servers='localhost')
server_topics = kafka_admin_client.list_topics()

print("List of topics:")
for topic in server_topics:
    print(topic)
