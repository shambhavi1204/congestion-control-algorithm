import time

class NewTCP:
    def __init__(self, start_rate=1000000, min_rate=1000000, max_rate=1000000000, c=0.4, beta=0.2, gamma=0.5):
        self.start_rate = start_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.c = c
        self.beta = beta
        self.gamma = gamma
        self.rtt = 0
        self.last_rtt = 0
        self.rate = start_rate

    def send(self):
        while True:
            # Send packets at current rate
            time.sleep(1 / self.rate)
            
            # Measure RTT
            self.last_rtt = self.rtt
            self.rtt = measure_rtt()
            
            # Detect congestion
            if self.rtt > self.last_rtt:
                self.rate = self.rate * (1 - self.beta * (self.last_rtt / self.rtt - 1) ** 3 - self.gamma * (self.rtt / self.last_rtt - 1))
                self.rate = max(self.rate, self.min_rate)
                self.rate = min(self.rate, self.max_rate)
            
            # Increase rate slowly
            else:
                self.rate = self.rate + self.c / (self.rate ** 0.5)
                self.rate = max(self.rate, self.min_rate)
                self.rate = min(self.rate, self.max_rate)
            
            # Periodically check for congestion
            if time.time() % 10 == 0:
                if self.rtt > self.last_rtt:
                    self.rate = self.rate * (1 - self.beta * (self.last_rtt / self.rtt - 1) ** 3 - self.gamma * (self.rtt / self.last_rtt - 1))
                    self.rate = max(self.rate, self.min_rate)
                    self.rate = min(self.rate, self.max_rate)
    
    def measure_rtt(self):
        # Measure RTT between packets
        return rtt

import simpy

# Simulation parameters
num_nodes = 10
switch_capacity = 1e9  # 1 Gbps
cbr_rate = 800e6  # 800 Mbps
simulation_time = 1000  # in seconds

# Define the network topology
class NetworkTopology:
    def __init__(self, env):
        self.env = env
        self.nodes = [simpy.Container(env, switch_capacity) for _ in range(num_nodes)]
    
    def send_packet(self, sender_id, receiver_id):
        # Calculate the time taken for the packet to reach the receiver
        rtt = 0.01  # simulated RTT
        yield self.env.timeout(rtt)
        
        # Update the receiver's buffer
        self.nodes[receiver_id].put(1)
        
        # Update the sender's congestion window
        # Use your proposed algorithm here
        
    def run_simulation(self):
        # Start the CBR traffic
        for i in range(num_nodes):
            self.env.process(self.cbr_traffic(i))
        
        # Start the simulation
        self.env.run(until=simulation_time)
        
    def cbr_traffic(self, sender_id):
        while True:
            # Wait for one second
            yield self.env.timeout(1)
            
            # Send a packet to a randomly chosen receiver
            receiver_id = sender_id
            while receiver_id == sender_id:
                receiver_id = random.randint(0, num_nodes-1)
            
            # Check if the sender's buffer is full
            if self.nodes[sender_id].level == 0:
                continue
            
            # Send the packet
            self.env.process(self.send_packet(sender_id, receiver_id))

# Define the TCP Reno protocol
class TCPReno:
    def __init__(self, env):
        self.env = env
        self.cwnd = 1
        
    def update_cwnd(self, rtt, congestion_occurred):
        if congestion_occurred:
            self.cwnd = 0.5 * self.cwnd
        else:
            self.cwnd = min(2 * self.cwnd, switch_capacity * rtt / 1500)
            
    def run_simulation(self, topology):
        while True:
            # Wait for one RTT
            rtt = 0.01  # simulated RTT
            yield self.env.timeout(rtt)
            
            # Check if congestion has occurred
            congestion_occurred = topology.nodes[0].level > self.cwnd
            
            # Update the congestion window
            self.update_cwnd(rtt, congestion_occurred)
            
            # Update the sender's buffer
            num_packets_sent = min(self.cwnd, topology.nodes[0].level)
            for i in range(num_packets_sent):
                topology.nodes[0].get(1)

# Define the TCP Vegas protocol
class TCPVegas:
    def __init__(self, env):
        self.env = env
        self.cwnd = 1
        
    def update_cwnd(self, rtt, congestion_occurred):
        if congestion_occurred:
            self.cwnd = 0.5 * self.cwnd
        else:
            self.cwnd = min(2 * self.cwnd, switch_capacity * rtt / 1500)
            
    def run_simulation(self, topology):
        while True:
            # Wait for one RTT
            rtt = 0.01  # simulated RTT
            yield self.env.timeout(rtt)
            
            # Check if congestion has occurred
            congestion_occurred

