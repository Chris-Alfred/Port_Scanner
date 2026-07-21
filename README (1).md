# 🔍 TCP Port Scanner

A simple, browser-based TCP port scanner built with Python and Streamlit.
Enter a target IP or hostname, choose a port range, and the app checks
each port with a TCP connect scan — showing live progress and a final
list of open ports.

## ⚠️ Legal & Ethical Use

Only scan hosts you **own** or have **explicit written permission** to
test. Scanning systems you don't have authorization for may violate
laws such as the U.S. Computer Fraud and Abuse Act (CFAA), the UK
Computer Misuse Act, or equivalent laws in your country — even if no
harm is done. When in doubt, don't scan it.

Good targets for practicing:
- `127.0.0.1` / `localhost` (your own machine)
- A VM or container you control on a private/local network
- Deliberately vulnerable practice targets designed for this purpose (e.g. a self-hosted lab environment)

## Features

- Simple web UI — no command-line arguments to remember
- Scans a configurable port range (1–65535)
- Adjustable timeout per port, so you can trade off speed vs. accuracy on slower/lossy networks
- Resolves hostnames to IP addresses before scanning, with a clear error if resolution fails
- Live progress bar and status updates as the scan runs
- Final table of open ports, plus total scan time

## How It Works

The scanner uses a **TCP connect scan**: for each port in the chosen
range, it attempts a full TCP connection using Python's built-in
`socket` module. If the connection succeeds (`connect_ex` returns `0`),
the port is considered open. This is the same basic technique used by
tools like `nmap`'s `-sT` scan — simple, reliable, and doesn't require
elevated/root privileges (unlike raw SYN scans).

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)

## Installation

```bash
# 1. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install streamlit
```

## How to Run

```bash
streamlit run app.py
```

This will open the app automatically in your browser at
`http://localhost:8501`. If it doesn't open automatically, copy that
URL into your browser manually.

## Usage

1. Enter a **target IP or hostname** (e.g. `127.0.0.1`)
2. Set the **timeout** per port (higher = more reliable on slow networks, but slower overall)
3. Choose a **start port** and **end port** to define the scan range
4. Click **Start Scan**
5. Watch the live progress bar, then review the list of open ports once the scan finishes

### Example

| Field       | Value       |
|-------------|-------------|
| Target      | `127.0.0.1` |
| Timeout     | `0.5`       |
| Start port  | `1`         |
| End port    | `100`       |

Example result:

```
Scan complete in 2.14s

Open Ports (3)
Port
22
80
443
```

## Notes & Limitations

- This is a **connect scan** only — it does not perform stealth (SYN),
  UDP, service/version detection, or OS fingerprinting scans.
- Large port ranges (e.g. full 1–65535) can take a while, since each
  port is scanned sequentially — there's no multithreading here by design, to keep the code simple and easy to follow.
- Scanning too fast or too broadly against a remote host may trigger
  intrusion detection systems (IDS) or firewalls, or get your IP
  blocked/rate-limited.
- Results can vary between runs on unreliable networks — a closed
  port and a filtered/firewalled port can sometimes be hard to tell
  apart with a basic connect scan.

## Possible Future Improvements

- Multithreaded/concurrent scanning for faster large-range scans
- UDP port scanning support
- Basic service/banner detection on open ports
- Export scan results to CSV/JSON
- Save scan history across sessions

## Disclaimer

This tool is provided for educational and authorized security testing
purposes only. The author(s) are not responsible for any misuse or
damage caused by this tool. Always obtain proper authorization before
scanning any network or system you do not own.
