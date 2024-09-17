import click
from database import UserDatabase
from utils import fetch_users, save_image
import csv
import os

db = UserDatabase()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--results', default=100, help='Number of users to fetch from the API.')
def import_users(results):
    """Fetches users from the API and stores them in the database."""
    users = fetch_users(results)
    db.insert_users(users)
    click.echo(f'Imported {len(users)} users.')

@cli.command()
@click.option('--file', default='users.csv', help='File name for exporting CSV.')
def export_users(file):
    """Exports users from the database to a CSV file."""
    users = db.get_all_users()
    with open(file, 'w', newline='') as csvfile:
        fieldnames = users[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)
    click.echo(f'Exported users to {file}.')

@cli.command()
@click.option('--first_name', default=None, help='Filter by first name.')
@click.option('--last_name', default=None, help='Filter by last name.')
def show_users(first_name, last_name):
    """Displays users from the database with optional filtering."""
    users = db.get_filtered_users(first_name, last_name)
    for user in users:
        #click.echo(f"{user['first_name']} {user['last_name']} ({user['email']})")
        click.echo(f"{user})")

@cli.command()
@click.option('--dir', default='images', help='Directory to store images.')
def download_images(dir):
    """Downloads user profile images to a local directory."""
    users = db.get_users_pictures()
    if not os.path.exists(dir):
        os.makedirs(dir)
    for user in users:
        save_image(user['medium'], os.path.join(dir, f"{user['user_id']}.jpg"))
    click.echo(f'Downloaded images to {dir}.')

if __name__ == '__main__':
    cli()
