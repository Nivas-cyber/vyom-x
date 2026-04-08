from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.layout import Layout
import random

console = Console()

def get_banner():
    banner_text = r"""
 [bold red]
  ██╗   ██╗██╗   ██╗ ██████╗ ███╗   ███╗      ██╗  ██╗
  ██║   ██║╚██╗ ██╔╝██╔═══██╗████╗ ████║      ╚██╗██╔╝
  ██║   ██║ ╚████╔╝ ██║   ██║██╔████╔██║ █████╗╚███╔╝ 
  ╚██╗ ██╔╝  ╚██╔╝  ██║   ██║██║╚██╔╝██║ ╚════╝██╔██╗ 
   ╚████╔╝    ██║   ╚██████╔╝██║ ╚═╝ ██║      ██╔╝ ██╗
    ╚═══╝     ╚═╝    ╚═════╝ ╚═╝     ╚═╝      ╚═╝  ╚═╝
 [/bold red]
 [bold white]Vyom-X v3.0 - Advanced & Professional Bug Hunting Suite[/bold white]
 [italic dim]Stealth, Speed, API Power, and Precision[/italic dim]
 [bold yellow]Created by @cyber-specterz[/bold yellow]
    """
    return Panel(Text.from_markup(banner_text), border_style="bold red", expand=False)

def display_banner():
    console.print(get_banner(), justify="center")

def print_success(message):
    console.print(f"[bold green][+][/bold green] {message}")

def print_status(message):
    console.print(f"[bold blue][*][/bold blue] {message}")

def print_error(message):
    console.print(f"[bold red][!][/bold red] {message}")

def print_warning(message):
    console.print(f"[bold yellow][!][/bold yellow] {message}")

def display_scan_results(target, results, os_type="Unknown"):
    table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("PORT", style="bold green", width=10)
    table.add_column("SERVICE", style="white")
    table.add_column("BANNER/VERSION", style="dim white")
    table.add_column("VULNERABILITY", justify="right")

    for res in results:
        v_status = res.get("vulnerabilities") or "[green]Secure[/green]"
        table.add_row(
            str(res.get("port")),
            res.get("service").upper(),
            res.get("version"),
            v_status
        )
    
    summary_text = Text.from_markup(
        f"[bold blue]Target:[/bold blue] {target}\n"
        f"[bold blue]OS:[/bold blue] {os_type}\n"
        f"[bold blue]Status:[/bold blue] [green]Scan Completed[/green]\n"
        f"[bold blue]Open Ports:[/bold blue] {len(results)}"
    )
    
    console.print("\n")
    console.print(Panel(summary_text, title="[bold white]PORT SCAN SUMMARY[/bold white]", border_style="bright_blue", expand=False))
    console.print(table)

def display_subdomains(target, subdomains):
    table = Table(show_header=True, header_style="bold magenta", border_style="dim")
    table.add_column("SUBDOMAIN", style="bold white")
    table.add_column("IP ADDRESS", style="cyan")

    for sub, ip in subdomains.items():
        table.add_row(sub, ip)

    console.print("\n")
    console.print(Panel(f"[bold blue]Target:[/bold blue] {target}\n[bold blue]Subdomains Found:[/bold blue] {len(subdomains)}", title="[bold white]SUBDOMAIN DISCOVERY[/bold white]", border_style="magenta", expand=False))
    console.print(table)

def display_fuzz_results(target, results):
    table = Table(show_header=True, header_style="bold yellow", border_style="dim")
    table.add_column("URL", style="bold white")
    table.add_column("STATUS", style="bold green")
    table.add_column("SIZE", style="dim white")

    for res in results:
        status_style = "green" if res['status'] < 300 else "yellow" if res['status'] < 400 else "red"
        table.add_row(
            res['url'],
            f"[{status_style}]{res['status']}[/{status_style}]",
            str(res['size'])
        )

    console.print("\n")
    console.print(Panel(f"[bold blue]Target:[/bold blue] {target}\n[bold blue]Assets Found:[/bold blue] {len(results)}", title="[bold white]DIRECTORY FUZZING[/bold white]", border_style="yellow", expand=False))
    console.print(table)
    console.print(f"\n[italic blue]Vyom-X v2.0 - Stealth mode active[/italic blue]\n")
