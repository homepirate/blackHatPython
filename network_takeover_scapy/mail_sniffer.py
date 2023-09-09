from scapy.all import sniff
from scapy.layers.inet import TCP, IP


def packet_callback(packet):
    # print(packet.show())
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            print(f'Destination: {packet[IP].dst}')
            print(str(packet[TCP].payload))


def main():
    # sniff(prn=packet_callback, count=1) all types packets
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143', prn=packet_callback, store=0)  # only 110, 25, 143 ports
                                                                                 # store=0 don`t store packets in memory


if __name__ == '__main__':
    main()
