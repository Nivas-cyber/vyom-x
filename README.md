<div align="center">
  <h1>Vyom-X v2.0 🌀</h1>
  <p><b>The Ultimate Advanced Professional Bug Hunting & Reconnaissance Suite</b></p>
  
  [![Python version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
  [![Maintained by](https://img.shields.io/badge/Maintained%20by-cyber--specterz-orange.svg)](https://github.com/cyber-specterz)
  [![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
</div>

---

## 📖 1. Tool Introduction

**Vyom-X v2.0** is a highly advanced, modular, and professional security auditing framework designed for bug hunters, penetration testers, and security researchers. Originally built as a simple reconnaissance engine, version 2.0 has been completely overhauled to deliver a powerful, all-in-one suite capable of executing deep-dive vulnerability analysis and high-speed asset discovery.

Designed with both power and ease-of-use in mind, Vyom-X streamlines complex ethical hacking workflows into a clean, rapid-fire command-line interface. Whether you are mapping out an entire corporate infrastructure or hunting for specific CVEs, Vyom-X provides the automation required to stay ahead of the curve.

---

## ⚙️ 2. Tool Specifications

Vyom-X v2.0 incorporates a rich set of features engineered for performance and accuracy:

*   **⚡ Multi-Threaded Core:** Optimized asynchronous execution for lighting-fast port scanning, fuzzing, and resolution.
*   **🌐 Subdomain Discovery:** Active resolution engine to uncover hidden, misconfigured, or forgotten subdomains.
*   **📂 Directory & Asset Fuzzing:** High-speed directory brute-forcing module to locate hidden administrative panels and forgotten assets.
*   **🛡️ Dynamic OS & Service Detection:** Intelligent heuristic fingerprinting and TTL analysis to accurately identify the target's operating system and running services.
*   **☢️ Advanced Vulnerability Engine:** Built-in, signature-based detection for critical exposures (e.g., *CVE-2021-41773, MS17-010 EternalBlue, BlueKeep, Anonymous FTP*).
*   **📊 Professional Reporting:** Automated generation of machine-readable `JSON` or structured `TXT` reports to seamlessly integrate with other pipeline tools.
*   **🎨 Stunning CLI:** Powered by `rich`, providing a flawless, color-coded terminal experience to make data parsing effortless for the human eye.

---

## 🛠️ 3. Tool Setup

Getting started with Vyom-X is simple and straightforward. Follow these steps to install the tool on your Linux, macOS, or Windows environment.

### Prerequisites
*   **Python 3.8** or higher
*   **Git** (optional, for cloning the repository directly)

### Step-by-Step Installation

**Step 1:** Clone the repository to your local machine.
```bash
git clone https://github.com/cyber-specterz/vyom-x.git
cd vyom-x
```

**Step 2:** Ensure your package manager is up to date and install the required dependencies.
```bash
pip install -r requirements.txt
# Alternatively, manually install the required modules:
# pip install requests rich
```

**Step 3:** Verify the installation by triggering the help menu.
```bash
python main.py -h
```

---

## 💻 4. Tool Usage

Vyom-X relies on intuitive command-line switches to give you precise control over your auditing payload.

### Quick Start: Basic Reconnaissance
Perform a standard port scan on the most common ports against a target:
```bash
python main.py -t example.com -p 1-1024
```

### The "Full Spectrum" Audit (Highly Recommended)
Launch all advanced modules concurrently—scanning all ports, performing vulnerability checks, hunting for subdomains, fuzzing directories, and saving the results to a structured text file:
```bash
python main.py -t target.com -p- -s -f -v -o txt
```

### Stealth & Speed: Quick Asset Discovery
Bypass heavy port mapping and immediately search for subdomains and hidden directories using a high thread count:
```bash
python main.py -t target.com -s -f -T 250
```

### Pipeline Integration
Run a clean scan and export the data directly to JSON for ingestion by other platforms or custom sorting scripts:
```bash
python main.py -t 10.0.0.5 -p 1-1000 -o json
```

---

## 🎛️ 5. Options Explanation

Below is a detailed breakdown of all available flags and their specific functions to help you customize your scans.

| Flag / Option | Long Name | Description | Example Target / Syntax |
| :--- | :--- | :--- | :--- |
| **`-t`** | `--target` | **(Required)** Specifies the IP address or domain name to scan. | `-t hackthissite.org` |
| **`-p`** | `--ports` | Defines the specific port range. Use comma separation for individuals, dashes for ranges, or `-p-` for all 65,535 ports. | `-p 80,443,8080` or `-p 1-1024` or `-p-` |
| **`-s`** | `--subdomains` | **(Toggle)** Activates the subdomain enumeration engine to map out related hostnames. | `-s` |
| **`-f`** | `--fuzz` | **(Toggle)** Activates the web directory fuzzing module to locate hidden endpoints. | `-f` |
| **`-v`** | `--vscan` | **(Toggle)** Triggers advanced vulnerability analysis against open ports and detected services. | `-v` |
| **`-o`** | `--output` | Save the final results to a file. Accepts `json` or `txt` formats in the auto-generated `outputs/` directory. | `-o json` |
| **`-T`** | `--threads` | Number of concurrent threads to deploy. Increase for faster scanning on robust networks. Default is `100`. | `-T 300` |

---

## ⚠️ Legal & Ethical Disclaimer

**Vyom-X is strictly designed for authorized security testing, educational purposes, and ethical hacking only.** 
Unauthorized scanning of networks and systems is illegal and punishable by law. The creator(s) and contributor(s) of this tool, including [@cyber-specterz](https://github.com/cyber-specterz), assume absolutely **NO liability** and are not responsible for any misuse, damage, or legal consequences caused by this software. Always ensure you have explicit, written permission from the system owner before executing Vyom-X.

---
<div align="center">
  <b>Developed by <a href="https://github.com/cyber-specterz">Cyber Specterz</a> | Empowering Security Professionals 🛡️</b>
</div>
