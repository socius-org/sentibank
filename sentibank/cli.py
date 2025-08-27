"""Command-line interface for sentibank."""
import argparse
import sys
import json
from typing import Optional
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from sentibank import archive
from sentibank.utils import analyze


console = Console()


def cmd_list(args: argparse.Namespace) -> int:
    """List available dictionaries and origins."""
    loader = archive.load()
    available = loader.list_available()
    
    # Create dictionaries table
    dict_table = Table(title="Available Dictionaries", show_header=True)
    dict_table.add_column("Index", style="cyan")
    dict_table.add_column("Type", style="green")
    
    for dict_name in available['dictionaries']:
        dict_type = dict_name.split('_')[0]
        dict_table.add_row(dict_name, dict_type)
    
    console.print(dict_table)
    
    # Create origins table
    if args.origins:
        origin_table = Table(title="\nAvailable Origin Datasets", show_header=True)
        origin_table.add_column("Index", style="cyan")
        origin_table.add_column("Type", style="green")
        
        for origin_name in available['origins']:
            origin_type = origin_name.split('_')[0]
            origin_table.add_row(origin_name, origin_type)
        
        console.print(origin_table)
    
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    """Analyze text using a sentiment dictionary."""
    try:
        analyzer = analyze()
        
        # Read text from file or stdin
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = args.text
        
        # Perform sentiment analysis
        result = analyzer.sentiment(text=text, dictionary=args.dictionary)
        
        # Format output
        if args.json:
            output = {
                'text': text[:100] + '...' if len(text) > 100 else text,
                'dictionary': args.dictionary,
                'result': result
            }
            print(json.dumps(output, indent=2))
        else:
            panel = Panel.fit(
                f"[bold]Text:[/bold] {text[:100]}{'...' if len(text) > 100 else ''}\n"
                f"[bold]Dictionary:[/bold] {args.dictionary}\n"
                f"[bold]Result:[/bold] {result}",
                title="Sentiment Analysis Result"
            )
            console.print(panel)
        
        return 0
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1


def cmd_info(args: argparse.Namespace) -> int:
    """Show information about a dictionary."""
    try:
        analyzer = analyze()
        
        console.print(f"\n[bold cyan]Dictionary Information: {args.dictionary}[/bold cyan]\n")
        analyzer.dictionary(dictionary=args.dictionary)
        
        return 0
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1


def cmd_export(args: argparse.Namespace) -> int:
    """Export a dictionary to a file."""
    try:
        loader = archive.load()
        
        # Load dictionary
        if args.format == 'json':
            data = loader.json(args.dictionary)
        else:
            data = loader.dict(args.dictionary)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = Path(f"{args.dictionary}.{args.format}")
        
        # Write to file
        if args.format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        elif args.format == 'csv':
            import pandas as pd
            df = pd.DataFrame.from_dict(data, orient='index', columns=['score'])
            df.index.name = 'word'
            df.to_csv(output_path)
        else:  # pickle
            import pickle
            with open(output_path, 'wb') as f:
                pickle.dump(data, f)
        
        console.print(f"[green]✓[/green] Exported {args.dictionary} to {output_path}")
        return 0
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='sentibank',
        description='Sentiment analysis using curated lexicons'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available dictionaries')
    list_parser.add_argument(
        '--origins',
        action='store_true',
        help='Also list available origin datasets'
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze sentiment of text')
    analyze_parser.add_argument('dictionary', help='Dictionary to use for analysis')
    analyze_parser.add_argument('text', nargs='?', help='Text to analyze')
    analyze_parser.add_argument(
        '-f', '--file',
        help='Read text from file instead of command line'
    )
    analyze_parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show dictionary information')
    info_parser.add_argument('dictionary', help='Dictionary to show info for')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export dictionary to file')
    export_parser.add_argument('dictionary', help='Dictionary to export')
    export_parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv', 'pickle'],
        default='json',
        help='Output format (default: json)'
    )
    export_parser.add_argument(
        '-o', '--output',
        help='Output file path'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute command
    commands = {
        'list': cmd_list,
        'analyze': cmd_analyze,
        'info': cmd_info,
        'export': cmd_export
    }
    
    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())