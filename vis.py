import random
import matplotlib.pyplot as plt

# Simulation parameters
MAX_BUFFER_SIZE = 10  
NUM_PACKETS = 100  
INITIAL_CWND = 1  
RTT = 10  
ALPHA = 15  
BETA = 4  # Beta parameter for TCP Vegas

# Simulation variables
cwnd = INITIAL_CWND
buffer = []
acked_packets = []
last_acked_packet = 0
last_rtt = 0
cwnd_values = []
unacked_packets = []

for i in range(NUM_PACKETS):
    # Send new packet
    if len(buffer) < MAX_BUFFER_SIZE and i > last_acked_packet:
        buffer.append(i)
    
    # Check if packet has been acknowledged
    if i in acked_packets:
        last_acked_packet = i
        buffer.remove(i)
        # Update congestion window size using TCP Vegas algorithm
        rtt = i - last_acked_packet
        if rtt < last_rtt:
            delta = ALPHA/cwnd
        else:
            delta = -BETA/cwnd
        cwnd += delta
        last_rtt = rtt
    else:
        # Packet has been lost or delayed
        # Decrease congestion window size by half
        cwnd /= 2
    
    # Simulate random acks
    if buffer:
        acked = random.sample(buffer, min(int(cwnd), len(buffer)))
        acked_packets.extend(acked)
        unacked_packets.append(len(buffer))
    else:
        unacked_packets.append(0)
    
    # Add current congestion window size to list of values
    cwnd_values.append(cwnd)
        
print("Simulation complete.")

# Create plot of congestion window size and unacknowledged packets over time
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time (packets)')
ax1.set_ylabel('Congestion Window Size (packets)', color=color)
ax1.plot(range(NUM_PACKETS), cwnd_values, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Unacknowledged Packets', color=color)
ax2.plot(range(NUM_PACKETS), unacked_packets, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('TCP Vegas Congestion Control')
plt.show()
