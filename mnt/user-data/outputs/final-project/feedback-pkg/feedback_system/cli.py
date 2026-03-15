import os
import click
from . import create_app, __version__
from .config import Config
from .database import init_db, export_csv, reset_db


def _env_config():
    env = os.environ.get('FLASK_ENV', 'production')
    return env if env in ('development', 'production', 'testing') else 'default'


@click.group()
@click.version_option(version=__version__, prog_name='feedback-system')
def cli():
    """Student Feedback System CLI."""
    pass


@cli.command()
@click.option('--host',   default=None, help='Host to bind (default: 0.0.0.0)')
@click.option('--port',   default=None, type=int, help='Port (default: 5000)')
@click.option('--debug',  is_flag=True, default=False, help='Enable debug mode')
@click.option('--config', 'config_name', default=None, help='development | production | testing')
def run(host, port, debug, config_name):
    """Start the Student Feedback web application."""
    cfg   = config_name or _env_config()
    app   = create_app(config=cfg)
    _host = host  or app.config.get('HOST',  '0.0.0.0')
    _port = port  or app.config.get('PORT',  5000)
    _dbg  = debug or app.config.get('DEBUG', False)

    click.echo(click.style(f'''
╔══════════════════════════════════════════╗
║  Student Feedback System v{__version__:<13}  ║
╠══════════════════════════════════════════╣
║  URL    : http://{_host}:{_port}
║  DB     : {app.config["DB_PATH"]}
║  Config : {cfg}
╚══════════════════════════════════════════╝
    ''', fg='green'))

    app.run(host=_host, port=_port, debug=_dbg)


@cli.command('init-db')
@click.option('--db-path', default=None, help='Path to the SQLite database')
def init_db_cmd(db_path):
    """Initialise the database."""
    path = db_path or os.environ.get('DB_PATH', Config.DB_PATH)
    init_db(path)
    click.echo(click.style(f'✓ Database initialised at: {path}', fg='green'))


@cli.command('export-csv')
@click.option('--db-path', default=None)
@click.option('--output',  default='feedback.csv')
def export_cmd(db_path, output):
    """Export all feedback to a CSV file."""
    path = db_path or os.environ.get('DB_PATH', Config.DB_PATH)
    data = export_csv(path)
    with open(output, 'w', newline='', encoding='utf-8') as f:
        f.write(data)
    lines = len(data.strip().split('\n')) - 1
    click.echo(click.style(f'✓ Exported {lines} records to: {output}', fg='green'))


@cli.command('reset-db')
@click.option('--db-path', default=None)
@click.confirmation_option(prompt='⚠  This will DELETE all feedback data. Continue?')
def reset_db_cmd(db_path):
    """Drop and recreate the database. ALL DATA WILL BE LOST."""
    path = db_path or os.environ.get('DB_PATH', Config.DB_PATH)
    reset_db(path)
    click.echo(click.style(f'✓ Database reset at: {path}', fg='yellow'))


@cli.command()
def info():
    """Show current configuration."""
    cfg = Config()
    click.echo(f'''
Student Feedback System v{__version__}
{"─" * 38}
DB_PATH    : {cfg.DB_PATH}
HOST       : {cfg.HOST}
PORT       : {cfg.PORT}
DEBUG      : {cfg.DEBUG}
PER_PAGE   : {cfg.PER_PAGE}
APP_NAME   : {cfg.APP_NAME}
SECRET_KEY : {'*** (set)' if cfg.SECRET_KEY != 'dev-secret-change-in-production' else '⚠  using default!'}
    ''')


def main():
    cli()


if __name__ == '__main__':
    main()
