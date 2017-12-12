from confluent_kafka import Producer
import subprocess
import re
import sys
import json



def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                         (msg.topic(), msg.partition(), msg.offset()))

def main(cmd="NOOP",
         pattern=".*",
         reportTo="https://kafka.innobubble.com",
         token="ENV_VAR",
         topic="GENERAL"):
    p = Producer({'bootstrap.servers': 'localhost:29092', 'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_PLAINTEXT',
                  'sasl.username': 'cherie', 'sasl.password' : 'cherie-secret'})
    #run a child process and read all its output
    #p = Producer({'bootstrap.servers': 'localhost:29092'})
    cli = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = 'begin capturing...'
    target = re.compile(pattern)
    while line:
        print(line)
        line = str(cli.stdout.readline(), 'utf-8')
        mobj = target.search(line)
        if mobj:
            print(':spotted: ' + line, end = "")
            capture = mobj.groupdict()
            print('::capture::' + str(capture), end ='\r\n')
            #now that we have our captured dictionary, lets pass it to kafka
            try:
                #the message payload can be string or bytes. Could just give str(capture)
                p.produce('general', json.dumps(capture), callback=delivery_callback)
            except BufferError as e:
                sys.stderr.write("Local producer queue is full, try again")
            p.poll(0)
    #len(p) returns the number of messages and kafka protocol requests waiting to be delivered to broker
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush() #wait for all messages in producer queue to be delivered


if __name__ == '__main__':
    print('running pyProducer as cli')
    main(*sys.argv[1:])