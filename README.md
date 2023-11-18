<h1 align="center">
  <img src="logo.png" alt="httpx" width="400px">
  <br>
</h1>

<p align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
<a href="https://twitter.com/DanialHalo"><img src="https://img.shields.io/twitter/follow/dan1337.svg?logo=twitter"></a>
<a href="https://www.linkedin.com/in/dan1337/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=whit"></a>
</p>

<p align="center">
  <a href="https://github.com/danialhalo/SqliSniper#key-features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="https://github.com/danialhalo/SqliSniper#running-sqlisniper">Running SqliSniper</a> •
  <a href="https://github.com/danialhalo/SqliSniper#contributing">Contributing</a> •
</p>

**SqliSniper** is a robust Python tool designed to detect time-based blind SQL injections in HTTP request headers. It enhances the security assessment process by rapidly scanning and identifying potential vulnerabilities using multi-threaded, ensuring speed and efficiency. Unlike other scanners, SqliSniper is designed to eliminates false positives through and send alerts upon detection, with the built-in Discord notification functionality.

![alt text](https://raw.githubusercontent.com/danialhalo/SqliSniper/main/banner.png)

## Key Features
- **Time-Based Blind SQL Injection Detection:** Pinpoints potential SQL injection vulnerabilities in HTTP headers.
- **Multi-Threaded Scanning:** Offers faster scanning capabilities through concurrent processing.
- **Discord Notifications:** Sends alerts via Discord webhook for detected vulnerabilities.
- **False Positive Checks:** Implements response time analysis to differentiate between true positives and false alarms.
- **Custom Payload and Headers Support:** Allows users to define custom payloads and headers for targeted scanning.


## Installation
```
git clone https://github.com/danialhalo/SqliSniper.git
cd SqliSniper
chmod +x sqlisniper.py
pip3 install -r requirements.txt
```
# Usage

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

# Running SqliSniper
### Single Url Scan
The url can be provided with `-u flag` for single site scan
```
./sqlisniper.py -u http://example.com
```
### File Input
The `-r flag` allows SqliSniper to read a file containing multiple URLs for simultaneous scanning.
```
./sqlisniper.py -r url.txt
```
### piping URLs
The SqliSniper can also worked with the pipeline input with `-p flag`
```
cat url.txt | ./sqlisniper.py -p
```
The pipeline feature facilitates seamless integration with other tools. For instance, you can utilize tools like subfinder and httpx, and then pipe their output to SqliSniper for mass scanning.
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
### Scanning with Single Payloads
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

---

<table>
<tr>
<td>

## Legal Disclaimer

Usage of this tool for attacking targets without prior mutual consent is strictly prohibited. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program..

</td>
</tr>
</table>

---

# Contributing
Contributions to SqliSniper are always welcome. Whether it's feature enhancements, bug fixes, or documentation improvements, every bit of help is appreciated.


# License
`SqliSniper` is distributed under [MIT License](https://github.com/danialhalo/SqliSniper/blob/main/LICENSE)

---

<div align="center">

`SqliSniper` is made in <img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png" alt="python" height="20px" width="20px"> with lots of 💙 by [@Muhammad Danial](https://twitter.com/DanialHalo).

</div>
