"""CLI entrypoint for DocWeave."""

import uvicorn

import click


@click.group()
def cli() -> None:
    """DocWeave - Documentation companion powered by GitHub Copilot CLI."""
    pass


@cli.command()
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind the server to",
    show_default=True,
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind the server to",
    show_default=True,
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development",
)
def serve(host: str, port: int, reload: bool) -> None:
    """Start the DocWeave web application server."""
    click.echo(f"🚀 Starting DocWeave server on http://{host}:{port}")
    click.echo("📖 Open your browser to view the application")
    click.echo("🛑 Press CTRL+C to stop the server")
    
    from docweave.app import app
    
    uvicorn.run(app, host=host, port=port, reload=reload)


def main() -> None:
    """Main entry point - runs the CLI."""
    cli()


if __name__ == "__main__":
    main()
