from typing import Dict, Any
import os
import sys

import typer

app = typer.Typer()
state: Dict[Any, Any] = {}

@app.command()
def greeting():
    typer.echo("Hello, this is objfunc.com client")

@app.callback()
def main(verbose: bool = False):
    state["verbose"] = verbose

if __name__ == "__main__":
    app()
