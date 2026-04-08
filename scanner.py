import socket
import threading
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

class OSDetector:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    def detect(self):
        """Optimized OS detection via TTL and ICMP"""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            wait_flag = "-w" if platform.system().lower() == "windows" else "-W"
            timeout = "1000" if platform.system().lower() == "windows" else "1"
            
            cmd = ["ping", param, "1", wait_flag, timeout, self.target_ip]
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=2).decode()
            
            if "ttl=" in output.lower():
                ttl_val = int(output.lower().split("ttl=")[1].split()[0])
                if ttl_val <= 64: return "Linux/Unix"
                if ttl_val <= 128: return "Windows"
                if ttl_val <= 255: return "Cisco/Network Device"
        except:
            pass
        return "Unknown"

class PortScanner:
    def __init__(self, target):
        self.target = target
        self._target_ip = self._resolve_target()

    def _resolve_target(self):
        try:
            return socket.gethostbyname(self.target)
        except:
            return self.target

    def scan(self, port_range, threads=100):
        ports = self._parse_port_range(port_range)
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task(f"Scanning {self.target}...", total=len(ports))
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {executor.submit(self._check_port_detailed, port): port for port in ports}
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception:
                        pass
                    progress.update(task, advance=1)
                
        return sorted(results, key=lambda x: x['port'])

    def _parse_port_range(self, port_range):
        if ',' in port_range:
            return [int(p.strip()) for p in port_range.split(',')]
        elif '-' in port_range:
            start, end = map(int, port_range.split('-'))
            return list(range(start, end + 1))
        else:
            return [int(port_range)]

    def _check_port_detailed(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.6)
                if s.connect_ex((self._target_ip, port)) == 0:
                    service = self._get_service_name(port)
                    banner = self._grab_banner(s, port)
                    
                    return {
                        "port": port,
                        "service": service,
                        "version": banner if banner else "Unknown",
                        "vulnerabilities": None
                    }
        except:
            pass
        return None

    def _grab_banner(self, sock, port):
        try:
            sock.settimeout(0.8)
            if port in [80, 443, 8080]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            
            banner = sock.recv(512).decode(errors='ignore').strip()
            banner = banner.split('\r\n')[0].split('\n')[0]
            return banner[:40] if banner else "Unknown"
        except:
            return "Unknown"

    def _get_service_name(self, port):
        try:
            overrides = {80: "http", 443: "https", 3389: "rdp", 3306: "mysql", 5432: "postgresql"}
            if port in overrides: return overrides[port]
            return socket.getservbyport(port)
        except:
            return "unknown"

class VulnerabilityEngine:
    @staticmethod
    def check(results):
        for res in results:
            port = res["port"]
            service = res["service"].lower()
            version = res["version"].lower()
            
            vulnerabilities = []
            if "apache" in version and "2.4.49" in version:
                vulnerabilities.append("[bold red]CVE-2021-41773 (Path Traversal)[/bold red]")
            if port == 445:
                vulnerabilities.append("[bold red]Potential SMB Vulnerability (MS17-010)[/bold red]")
            if port == 3389:
                vulnerabilities.append("[bold yellow]RDP Exposed (Check for BlueKeep)[/bold yellow]")
            if "ssh" in service:
                vulnerabilities.append("[bold cyan]SSH Found - Brute-force auditing recommended[/bold cyan]")
            if port == 21:
                vulnerabilities.append("[bold yellow]FTP Found - Check for anonymous login[/bold yellow]")
            
            res["vulnerabilities"] = ", ".join(vulnerabilities) if vulnerabilities else "[green]Secure[/green]"
        return results
