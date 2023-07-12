import time
import random

# Define constants
MAX_THROUGHPUT = 800 # in Mbps
NODES = 10
SWITCH_CAPACITY = 1000 # in Mbps
SEND_RATE_STEP = 10 # in Mbps
CONGESTION_THRESHOLD = 100 # in ms
BACKOFF_FACTOR = 0.5
FAIR_QUEUE_THRESHOLD = SWITCH_CAPACITY / NODES

# Define classes
class Packet:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.timestamp = time.time()

class NetworkConnection:
    def __init__(self, bandwidth):
        self.bandwidth = bandwidth
        self.queue = []

    def send_packet(self, packet):
        self.queue.append(packet)

    def recv_ack(self):
        if len(self.queue) > 0:
            packet = self.queue.pop(0)
            rtt = (time.time() - packet.timestamp) * 1000 # in ms
            return rtt
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0

class CongestionControl:
    def __init__(self, connections):
        self.connections = connections
        self.sending_rate = 10 # in Mbps
        self.rtt_samples = []
        self.last_congestion = 0
        self.fair_queue_threshold = FAIR_QUEUE_THRESHOLD
        self.node_count = len(connections)
        self.max_throughput = MAX_THROUGHPUT
        self.send_rate_step = SEND_RATE_STEP
        self.backoff_factor = BACKOFF_FACTOR
        self.packet_size = 1500
        self.packet_bits = self.packet_size * 8

    def send_packets(self):
        for conn in self.connections:
            bits_sent = len(conn.queue) * self.packet_bits
            bits_to_send = self.sending_rate * 1000000 - bits_sent
            packets_to_send = bits_to_send // self.packet_bits
            for i in range(int(packets_to_send)):
                packet = Packet(random.randint(1, 10000), self.packet_size)
                conn.send_packet(packet)

    def cubic(self, t):
        k = 0.0025
        beta = 0.7
        return (self.sending_rate * (t - self.last_congestion - k * (t - self.last_congestion)**2)) / (self.sending_rate * (1 - beta) + beta * (t - self.last_congestion - k * (t - self.last_congestion)**2))

    def backoff(self):
        self.sending_rate = self.sending_rate * self.backoff_factor

    def fair_queue(self):
        queue_sizes = [len(conn.queue) for conn in self.connections]
        min_queue_size = min(queue_sizes)
        max_queue_size = max(queue_sizes)
        if min_queue_size == 0:
            fairness = float('inf')
        else:
            fairness = max_queue_size / min_queue_size

    # Send packets
        for conn in self.connections:
            while not conn.is_empty() and len(conn.queue) <= fairness:
                packet = conn.queue.pop(0)
                for i in range(NODES):
                    if sum([len(c.queue) for c in self.connections]) < FAIR_QUEUE_THRESHOLD:
                        self.connections[i].send_packet(packet)
                        break



    def run(self):
        start_time = time.time()
        while time.time() - start_time < 60: # run for 1 minute
            # Send packets
            self.send_packets()

            # Check for acknowledgments
            for conn in self.connections:
                rtt = conn.recv_ack()
                if rtt:
                    self.rtt_samples.append(rtt)

            # Check for congestion
            if len(self.rtt_samples) > 0 and max(self.rtt_samples) > CONGESTION_THRESHOLD:
                self.backoff()
                self.last_congestion = time.time()

            # Update sending rate
            if time.time() - self.last_congestion > 10:
                t = time.time() - self.last_congestion - 10
                self.sending_rate = min(self.sending_rate + self.send_rate_step * self.cubic(t), self.max_throughput)

            # Fair queue
            self.fair_queue()



        print("Algorithm simulation complete.")


import matplotlib.pyplot as plt

# Define simulation function
def simulate_algorithm(algorithm_name, connections):
    algorithm = CongestionControl(connections)
    algorithm.run()
    throughput = sum([len(conn.queue) for conn in connections]) * 1500 * 8 / 1000000
    fairness = max([len(conn.queue) for conn in connections]) / min([len(conn.queue) for conn in connections])
    print("{} - Throughput: {:.2f} Mbps, Fairness: {:.2f}".format(algorithm_name, throughput, fairness))
    return throughput, fairness

# Set up network connections
connections = [NetworkConnection(SWITCH_CAPACITY / NODES) for _ in range(NODES)]

# Simulate CongestionControl algorithm
cc_throughput, cc_fairness = simulate_algorithm("CongestionControl", connections)

# Simulate TCP Reno
reno_connections = [NetworkConnection(SWITCH_CAPACITY / NODES) for _ in range(NODES)]
reno_throughput, reno_fairness = simulate_algorithm("TCP Reno", reno_connections)

# Simulate TCP Vegas
vegas_connections = [NetworkConnection(SWITCH_CAPACITY / NODES) for _ in range(NODES)]
vegas_throughput, vegas_fairness = simulate_algorithm("TCP Vegas", vegas_connections)

# Simulate TCP Cubic
cubic_connections = [NetworkConnection(SWITCH_CAPACITY / NODES) for _ in range(NODES)]
cubic_throughput, cubic_fairness = simulate_algorithm("TCP Cubic", cubic_connections)

# Plot results
labels = ["CongestionControl", "TCP Reno", "TCP Vegas", "TCP Cubic"]
throughputs = [cc_throughput, reno_throughput, vegas_throughput, cubic_throughput]
fairnesses = [cc_fairness, reno_fairness, vegas_fairness, cubic_fairness]
fig, ax = plt.subplots()
ax.bar(labels, throughputs, label="Throughput")
ax.bar(labels, fairnesses, label="Fairness")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Throughput (Mbps) / Fairness")
ax.set_title("Algorithm Performance Comparison")
ax.legend()
plt.show()

