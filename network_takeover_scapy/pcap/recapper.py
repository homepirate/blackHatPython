import collections
import os
import re
import sys
import zlib

from scapy.all import rdpcap
from scapy.layers.inet import TCP

OUTDIR = 'pictures'
PCAPS = ''


Response = collections.namedtuple('Response', ['header', 'payload'])


def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-'*30)
        sys.stdout.flush()
        return None

    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))

    if 'Content-type' not in header:
        return None
    return header


def extract_content(response: Response, content_name='image'):
    content, content_type = None, None
    if content_name in response.header['Content-type']:
        content_type = response.header['Content-type'].split('/')[1]
        content = response.payload[response.payload.index(b'\r\n\r\n')+4:]

        if 'Content-Encoding' in response.header:
            if response.header['Content-Encoding'] == 'gzip':
                content = zlib.decompress(response.payload, zlib.MAX_WBITS | 32)
            elif response.header['Content-Encoding'] == 'default':
                content = zlib.decompress(response.payload)
    return content, content_type


class Recapper:
    def __init__(self, fname):
        pcap = rdpcap(fname)
        self.sessions = pcap.sessions()
        self.responses = list()

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].pyload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()
            if payload:
                header = get_header(payload)
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload))

    def write(self, content_name):
        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                file_name = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'Eriting {file_name}')
                with open(file_name, 'wb') as file:
                    file.write(content)


def main():
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')


if __name__ == '__main__':
    main()
