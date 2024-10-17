import os
from rich.console import Console
from rich.panel import Panel
from ctfile_downloader.utils import load_config, create_directories
from ctfile_downloader.downloader import process_links

console = Console()


def display_header():
    """Displays a rich-style header for the CTFile Downloader."""
    header_text = (
        "[bold magenta]🚀 CTFile Downloader Pro[/bold magenta]\n"
        "[bold white]📝 Version 1.0.0[/bold white]\n"
        "[bold cyan]👤 by SSujitX [/bold cyan]\n"
        "[bold blue]🔗 GitHub: https://github.com/SSujitX[/bold blue]"
    )
    console.print(
        Panel(header_text, expand=False, border_style="blue", title="🌟 CTFILE 🌟")
    )


def validate_link(link):
    """Checks if a link starts with 'http' or 'https'."""
    if not (link.startswith("http://") or link.startswith("https://")):
        return False
    return True


def main():
    display_header()  # Show the header when the program starts

    config_path = "config.yml"
    config = load_config(config_path)
    create_directories(config)

    while True:
        # Using console.input to make the input prompt styled and engaging
        user_input = console.input(
            "[bold yellow]Enter CTFile Link (or Press Enter For Batch Links): [/bold yellow]"
        )

        if user_input:
            url_list = user_input.split(",")
            invalid_urls = [url for url in url_list if not validate_link(url.strip())]

            if invalid_urls:
                console.print(
                    f"\n[bold red]Error:[/bold red] The following links are invalid because they don't start with 'http' or 'https':\n"
                    f"[bold red]{invalid_urls}[/bold red]\n"
                    "[bold yellow]Please enter valid URLs starting with 'http://' or 'https://'.[/bold yellow]\n"
                )
                continue  # Re-prompt the user for valid input
        else:
            # Batch processing: read all text files in the batch folder
            batch_folder = config["batch_folder"]
            batch_text_files = [
                f for f in os.listdir(batch_folder) if f.endswith(".txt")
            ]
            if len(batch_text_files) == 0:
                console.print(
                    "\n[bold red]No text files found in the batch folder.\n"
                    "Please add text files to the batch folder and try again.[/bold red]\n"
                )
                continue  # No batch files, so re-prompt for user input

            url_list = []
            for text_file in batch_text_files:
                with open(f"{batch_folder}/{text_file}", "r") as file:
                    urls = file.read().splitlines()
                    url_list.extend(urls)

            # Validate batch links
            invalid_urls = [url for url in url_list if not validate_link(url.strip())]
            if invalid_urls:
                console.print(
                    f"\n[bold red]Error:[/bold red] The following batch links are invalid because they don't start with 'http' or 'https':\n"
                    f"[bold red]{invalid_urls}[/bold red]\n"
                    "[bold yellow]Please correct the URLs in the batch files.[/bold yellow]\n"
                )
                continue

        process_links(url_list, config)


if __name__ == "__main__":
    main()
