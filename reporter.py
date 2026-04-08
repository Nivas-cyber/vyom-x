import json
import datetime

class Reporter:
    def __init__(self, target):
        self.target = target
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_json(self, data, filename=None):
        if not filename:
            filename = f"vyom_report_{self.target}_{self.timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return filename
        except Exception as e:
            return f"Error: {e}"

    def export_text(self, data, filename=None):
        if not filename:
            filename = f"vyom_report_{self.target}_{self.timestamp}.txt"
            
        try:
            with open(filename, 'w') as f:
                f.write(f"Vyom-X Scan Report\n")
                f.write(f"==================\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if 'ports' in data:
                    f.write("Port Scan Results:\n")
                    f.write("------------------\n")
                    for res in data['ports']:
                        f.write(f"Port: {res['port']} | Service: {res['service']} | Version: {res['version']} | Vuln: {res['vulnerabilities']}\n")
                    f.write("\n")
                
                if 'subdomains' in data:
                    f.write("Subdomain Discovery:\n")
                    f.write("--------------------\n")
                    for sub, ip in data['subdomains'].items():
                        f.write(f"{sub} -> {ip}\n")
                    f.write("\n")
                    
                if 'fuzz' in data:
                    f.write("Directory Fuzzing:\n")
                    f.write("------------------\n")
                    for res in data['fuzz']:
                        f.write(f"URL: {res['url']} | Status: {res['status']} | Size: {res['size']}\n")
                    f.write("\n")
            return filename
        except Exception as e:
            return f"Error: {e}"
