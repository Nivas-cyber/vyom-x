import sys
import argparse
import socket
from ui import display_banner, print_status, print_success, print_error, display_scan_results, display_subdomains, display_fuzz_results
from scanner import PortScanner, OSDetector, VulnerabilityEngine
from subdomain import SubdomainScanner
from fuzzer import DirFuzzer
from reporter import Reporter

def main():
    display_banner()
    
    parser = argparse.ArgumentParser(description="Vyom-X v2.0: The Ultimate Bug Hunting Suite")
    parser.add_argument("-t", "--target", help="Target IP address or domain", required=True)
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1024 or -p- for all)", default=None)
    parser.add_argument("-s", "--subdomains", help="Enable subdomain enumeration", action="store_true")
    parser.add_argument("-f", "--fuzz", help="Enable directory fuzzing", action="store_true")
    parser.add_argument("-v", "--vscan", help="Enable vulnerability scanning", action="store_true")
    parser.add_argument("-o", "--output", help="Export results (json/txt)", choices=['json', 'txt'])
    parser.add_argument("-T", "--threads", help="Number of concurrent threads (default: 100)", type=int, default=100)
    
    args = parser.parse_args()
    
    target = args.target
    scan_data = {"target": target, "timestamp": None}
    
    try:
        # Resolve target IP for OS detection
        try:
            target_ip = socket.gethostbyname(target)
        except:
            target_ip = target

        os_detector = OSDetector(target_ip)
        os_type = os_detector.detect()
        scan_data["os"] = os_type
        print_status(f"Target: [bold cyan]{target}[/bold cyan] ([dim]{target_ip}[/dim]) | OS: [bold magenta]{os_type}[/bold magenta]")

        # 1. Port Scanning
        if args.ports:
            port_range = "1-65535" if args.ports == "-" else args.ports
            print_status(f"Phase 1: Port Scanning & Service Identification ({port_range})...")
            p_scanner = PortScanner(target)
            results = p_scanner.scan(port_range, threads=args.threads)
            
            if results:
                if args.vscan:
                    print_status("Phase 1.1: Vulnerability Analysis...")
                    results = VulnerabilityEngine.check(results)
                
                scan_data["ports"] = results
                display_scan_results(target, results, os_type)
            else:
                print_error("No open ports found or target unreachable.")

        # 2. Subdomain Enumeration
        if args.subdomains:
            print_status("Phase 2: Subdomain Discovery...")
            s_scanner = SubdomainScanner(target)
            found_subs = s_scanner.scan(threads=args.threads // 2)
            if found_subs:
                scan_data["subdomains"] = found_subs
                display_subdomains(target, found_subs)
            else:
                print_status("No subdomains discovered with default wordlist.")

        # 3. Directory Fuzzing
        if args.fuzz:
            print_status("Phase 3: Directory & Asset Fuzzing...")
            fuzzer = DirFuzzer(target)
            fuzz_results = fuzzer.fuzz(threads=args.threads // 2)
            if fuzz_results:
                scan_data["fuzz"] = fuzz_results
                display_fuzz_results(target, fuzz_results)
            else:
                print_status("No interesting assets found with default wordlist.")

        # 4. Reporting
        if args.output:
            reporter = Reporter(target)
            if args.output == 'json':
                filename = reporter.export_json(scan_data)
            else:
                filename = reporter.export_text(scan_data)
            print_success(f"Report exported to: [bold white]{filename}[/bold white]")

        print_success("All requested tasks completed!")
        
    except KeyboardInterrupt:
        print_error("\nOperation aborted by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
