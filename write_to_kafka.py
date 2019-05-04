from kafka import KafkaProducer
import json, sys


def getData(fileName, topic_name):
    lines = open(file=fileName,mode="r").readlines()
    producer_instance = connect_kafka_producer()
    i =0
    for line in lines:
        if line is None or line.strip().__len__() ==0:
            continue
        for data in json.loads(line):
            key_bytes = bytes('foo', encoding='utf-8')
            value_bytes = bytes(json.dumps(data), encoding='utf-8')
            producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
            producer_instance.flush(10000)
            i = i+1
            if i %100 ==0:
                print("No. of messages published to kafka so far:",i)
    print("No of messages published to kafka in Total:", i)
    producer_instance.flush(10000)
    producer_instance.close()
    return None

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10), linger_ms=10)

    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print('Number of arguments is not correct. We have 2 arguments absolutefilepath kafka_topic_name')
        exit()

    file_name = sys.argv[1]
    topic_name = sys.argv[2]
    getData(fileName=file_name, topic_name=topic_name)
