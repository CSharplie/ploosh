"""Automatized Testing Framework"""

from execute import execute




#console = Console()
#
#table = Table(box=None, show_header=False, expand=True, padding=(0, 2))
#table.add_column("Nom du Test", style="dim", no_wrap=True)
#table.add_column("Statut", no_wrap=True)
#table.add_column("Spacer", ratio=1)
#table.add_column("Durée", justify="right", no_wrap=True)
#
#table.add_row("test_ingestion_lakehouse", "[bold green]PASS[/]", "", "1.24s")
#table.add_row("test_transformation_gold", "[bold red]FAIL[/]", "", "4.50s")
#table.add_row("test_schema_validation", "[bold green]PASS[/]", "", "0.85s")
#
#console.print(table)





def main():
    """Entry point for conda execution"""
    # Call the main execution function
    execute()


# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main execution function
    main()
