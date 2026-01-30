import argparse
from pathlib import Path
from .parser import ChatParser
from .analyzer import ChatAnalyzer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.align import Align
from rich.progress import track
from rich.layout import Layout
from rich import box

console = Console()

def print_banner():
    """Print an attractive banner."""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║  💬  CHAT HISTORY ANALYZER  💬           ║
    ║     Unlock Your Chat Insights             ║
    ╚═══════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")

def main():
    parser = argparse.ArgumentParser(description="Analyze chat history files.")
    parser.add_argument('file', help="Path to the chat history file")
    parser.add_argument('--output', '-o', help="Output file for the report", default=None)
    parser.add_argument('--top-words', '-w', type=int, default=10, help="Number of top words to show")

    args = parser.parse_args()

    print_banner()

    file_path = Path(args.file)
    if not file_path.exists():
        console.print(f"[red bold]✗ Error: File {file_path} does not exist.[/red bold]")
        return

    # Parse the chat
    console.print(f"[cyan]📂 Loading chat file: {file_path}[/cyan]")
    chat_parser = ChatParser(str(file_path))
    messages = chat_parser.parse()

    if not messages:
        console.print("[yellow bold]⚠ No messages found in the file. Check the format.[/yellow bold]")
        return

    console.print(f"[green]✓ Found {len(messages)} messages![/green]\n")

    # Analyze
    analyzer = ChatAnalyzer(messages)

    # Display results with panels
    layout = Layout()
    layout.split_column(
        Layout(name="header"),
        Layout(name="main")
    )

    # Message count table
    msg_count = analyzer.get_message_count_per_user()
    table = Table(title="📊 Messages per User", box=box.HEAVY, padding=(0, 2))
    table.add_column("👤 User", style="bold cyan")
    table.add_column("💬 Count", style="bold magenta", justify="right")
    
    total_msgs = sum(msg_count.values())
    for user, count in sorted(msg_count.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_msgs) * 100
        bar_length = int(percentage / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        table.add_row(user, f"{count} ({percentage:.1f}%) {bar}")
    console.print(table)

    # Top words
    word_freq = analyzer.get_word_frequency(args.top_words)
    table = Table(title=f"🔤 Top {args.top_words} Words", box=box.HEAVY, padding=(0, 2))
    table.add_column("Word", style="bold cyan")
    table.add_column("Frequency", style="bold magenta", justify="right")
    
    max_freq = word_freq[0][1] if word_freq else 1
    for word, freq in word_freq:
        percentage = (freq / max_freq) * 100
        bar_length = int(percentage / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        table.add_row(word, f"{freq} {bar}")
    console.print(table)

    # Stats
    avg_len = analyzer.get_average_message_length()
    
    stats_panel = Panel(
        f"[bold green]✓ Analysis Complete![/bold green]\n\n"
        f"[cyan]📈 Total Messages:[/cyan] [bold yellow]{len(messages)}[/bold yellow]\n"
        f"[cyan]📏 Average Length:[/cyan] [bold yellow]{avg_len:.2f}[/bold yellow] characters\n"
        f"[cyan]👥 Active Users:[/cyan] [bold yellow]{len(msg_count)}[/bold yellow]",
        title="[bold]📋 Summary Statistics[/bold]",
        border_style="bold green",
        padding=(1, 2)
    )
    console.print(stats_panel)

    # Generate report
    report = analyzer.generate_report()
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        success_panel = Panel(
            f"[bold green]✓ Report successfully saved![/bold green]\n"
            f"[cyan]📄 Location:[/cyan] [bold yellow]{args.output}[/bold yellow]",
            border_style="bold green",
            padding=(1, 2)
        )
        console.print(success_panel)
    else:
        console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold]📋 FULL REPORT[/bold]")
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        console.print(report)

if __name__ == "__main__":
    main()