# ping_exporter

A simple Prometheus exporter that pings a target

## Usage

**Runs with Python 3**

```
$ pip install -r requirements.txt
$ python3 exporter.py --help
usage: exporter.py [-h] [--debug] [--port PORT] --target TARGET [--icmp]
                   [--tcp TCP [TCP ...]] [--frequency FREQUENCY]

Run

optional arguments:
  -h, --help            show this help message and exit
  --debug, -v           Enable debug mode
  --port PORT, -p PORT  Port to listen on
  --target TARGET, -t TARGET
                        Target of the exporter
  --icmp                Ping target
  --tcp TCP [TCP ...]   Test TCP connection to this port
  --frequency FREQUENCY, -f FREQUENCY
                        Frequency of target pinging in seconds
```

## With Docker

**Needs NET_RAW capability**

```bash
$ docker run -d -p 9123:9123 --cap-add NET_RAW oxalide/ping_exporter:latest --target www.oxalide.com --icmp --tcp 80 443
$ http localhost:9123/metrics
HTTP/1.0 200 OK
Content-Type: text/plain; version=0.0.4; charset=utf-8
Date: Fri, 02 Jun 2017 15:18:34 GMT
Server: BaseHTTP/0.6 Python/3.5.2

# HELP ping_round_trip Time of round-trip ping to target
# TYPE ping_round_trip gauge
ping_round_trip{target="www.oxalide.com"} 11.976
# HELP ping_return_code ICMP return code
# TYPE ping_return_code gauge
ping_return_code{target="www.oxalide.com"} 0.0
# HELP tcp_connect Can open a socket to a port
# TYPE tcp_connect gauge
tcp_connect{port="443",target="www.oxalide.com"} 1.0
tcp_connect{port="80",target="www.oxalide.com"} 1.0
```
