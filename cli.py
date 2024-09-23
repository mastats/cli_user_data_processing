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
    headers = users[0].__table__.columns.keys()
    with open(file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for user in users:
            writer.writerow([getattr(user, column) for column in headers])
    click.echo(f'Exported users to {file}.')

@cli.command()
@click.option('--user_id', default=None, help='Filter by user ID.')
@click.option('--first_name', default=None, help='Filter by first name.')
@click.option('--last_name', default=None, help='Filter by last name.')
@click.option('--age', default=None, help='Filter by age.')
@click.option('--country', default=None, help='Filter by country.')
def show_users(user_id, first_name, last_name, age, country):
    """Displays users from the database with optional filtering."""
    users = db.get_filtered_users(user_id, first_name, last_name, age, country)
    for user in users:
        click.echo(f"ID: {user.user_id}, Name: {user.first_name} {user.last_name}, Country: {user.location.country}, Temperature: {user.location.temperature}")

@cli.command()
@click.option('--dir', default='images', help='Directory to store images.')
@click.option('--size', default='medium', type=click.Choice(['large', 'medium', 'thumbnail']), help='Images size')
def download_images(dir, size):
    """Downloads user profile images to a local directory."""
    users = db.get_users_pictures(size=size)
    if not os.path.exists(dir):
        os.makedirs(dir)
    for user_id, image_url in users: #tuple
        #print(image_url)
        save_image(image_url, os.path.join(dir, f"{user_id}.jpg"))
    click.echo(f'Downloaded images to {dir}.')

if __name__ == '__main__':
    cli()
