import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

class DirFuzzer:
    def __init__(self, target):
        # Ensure target has protocol
        if not target.startswith(("http://", "https://")):
            self.target = f"http://{target}"
        else:
            self.target = target
        
        self.default_wordlist = [
            "admin", "login", "config", "backup", "api", "v1", "v2", 
            "wp-admin", "index.php", "phpinfo.php", ".env", ".git", 
            "robots.txt", "sitemap.xml", "assets", "js", "css", "img"
        ]

    def fuzz(self, wordlist=None, threads=20):
        words = wordlist if wordlist else self.default_wordlist
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task(f"Fuzzing directories on {self.target}...", total=len(words))
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                # Add a trailing slash for the base target if not present for easier joining
                base_url = self.target.rstrip("/")
                futures = {executor.submit(self._check_path, f"{base_url}/{word}"): word for word in words}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    progress.update(task, advance=1)
                    
        return results

    def _check_path(self, url):
        try:
            # Use a realistic User-Agent to avoid some basic blocks
            headers = {'User-Agent': 'Vyom-X Recon Engine/2.0'}
            response = requests.get(url, headers=headers, timeout=3, allow_redirects=False)
            
            # We report 200, 301, 302, 403 (could be interesting)
            if response.status_code in [200, 301, 302, 403]:
                return {
                    "url": url,
                    "status": response.status_code,
                    "size": len(response.content)
                }
        except:
            pass
        return None
