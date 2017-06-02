import argparse
import coloredlogs
import logging
import pyping
import time
import socket
from prometheus_client import start_http_server, Gauge


def metrics(icmp_gauge=None, icmp_code_gauge=None, tcp_gauge=None):
    if cli.icmp:
        r = pyping.ping(cli.target, count=1)
        if r.avg_rtt is not None:
            icmp_gauge.labels(cli.target).set(r.avg_rtt)
        icmp_code_gauge.labels(cli.target).set(r.ret_code)
    if cli.tcp:
        for port in cli.tcp:
            s = socket.socket()
            s.settimeout(1)
            try:
                s.connect((cli.target, port))
                tcp_gauge.labels(cli.target, port).set(1)
            except Exception as e:
                tcp_gauge.labels(cli.target, port).set(0)
            finally:
                s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run")
    parser.add_argument('--debug', '-v',
                        action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--port', '-p',
                        default=9123,
                        help='Port to listen on')
    parser.add_argument('--target', '-t',
                        required=True,
                        help='Target of the exporter')
    parser.add_argument('--icmp',
                        action='store_true',
                        help='Ping target')
    parser.add_argument('--tcp',
                        default=None, type=int, nargs='+',
                        help='Test TCP connection to this port')
    parser.add_argument('--frequency', '-f',
                        default=15,
                        help='Frequency of target pinging in seconds')

    cli = parser.parse_args()
    logger = logging.getLogger('run')
    if cli.debug:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'

    if cli.icmp:
        icmp_gauge = Gauge('ping_round_trip',
                           'Time of round-trip ping to target',
                           ['target'])
        icmp_code_gauge = Gauge('ping_return_code',
                                'ICMP return code',
                                ['target'])
    else:
        icmp_gauge = None

    if cli.tcp:
        tcp_gauge = Gauge('tcp_connect',
                          'Can open a socket to a port',
                          ['target', 'port'])
    else:
        tcp_gauge = None

    coloredlogs.install(level=log_level)
    start_http_server(cli.port)
    while True:
        logger.info('Scrapping target %s', cli.target)
        metrics(icmp_gauge=icmp_gauge, icmp_code_gauge=icmp_code_gauge,
                tcp_gauge=tcp_gauge)
        time.sleep(cli.frequency)
