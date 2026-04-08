import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

class SubdomainScanner:
    def __init__(self, target):
        self.target = target
        self.subdomains = []
        # Small default wordlist for demo/initial use
        self.default_wordlist = ["www", "dev", "test", "staging", "api", "mail", "blog", "vpn", "admin", "portal"]

    def scan(self, wordlist=None, threads=20):
        words = wordlist if wordlist else self.default_wordlist
        found = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task(f"Enumerating subdomains for {self.target}...", total=len(words))
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {executor.submit(self._check_subdomain, word): word for word in words}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        found[result[0]] = result[1]
                    progress.update(task, advance=1)
        
        return found

    def _check_subdomain(self, word):
        subdomain = f"{word}.{self.target}"
        try:
            ip = socket.gethostbyname(subdomain)
            return (subdomain, ip)
        except:
            return None
