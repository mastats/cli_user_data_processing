# CLI to fetch user data
CLI app that interacts with an external API to fetch user data (https://randomuser.me/api/).
This app is designed for an environment running Python 3.9.6. 

## Setup

1. Clone the Repository:
```bash
git clone https://github.com/mastats/cli_user_data_processing.git
cd random_user_cli
```

2. Install Dependencies:
Install the dependencies in the requirements file (Requests & Click)
```bash 
pip install -r requirements.txt
```

3. Run the CLI:
Run the CLI app an checkout the --help for a list of available commands.
```bash
python cli.py --help
```
## Commands

1. Import Users:
Fetch and import users from the API into the database. You can use the --results argument to define how many users are to be fetched.
```bash
python cli.py import_users --results 100
```

2. Export Users:
Exports all users to a CSV file. You can use the --file argument to set the name of the output file.
```bash
python cli.py export_users --file users.csv
```

3. Show Users:
Show all users or filter by first name, last name.
```bash
python cli.py show_users --first_name John --last_name Doe
```

4. Download Images:
Download all user profile images to a local directory. You can use the --dir argument to set the name of the directory. The app will create the necessary folders for you. 
```bash
python cli.py download_images --dir ./images
```

## Containerization
You can also run this solution from a container. Check the Dockerfile included in this repository to build the image and run it from your laptop of preferred Docker service.

1. Build the Docker image:
```bash
docker build -t random_user_cli .
```

2. Run the CLI app inside the container:
```bash
docker run -it random_user_cli python cli.py import_users --results 100
```

## Design & asumptions
### Data model
All the fetched data is structured and stored in a normalized way by using the following tables:
1. **Users**
2. **Locations.**
3. **Logins**
4. **IDs**
5. **Pictures**

Model details:
* The main table is Users and all other tables have user_id as a foreign key. This allows for a natural flow of information where the user ID should come first and then locations, logins, pictures or any other information tied to them. 
* This model reduces redundancy since each table stores distinct data, solves partial dependencies and makes data updates flexible.
* Transactional inserts are used to ensure atomicity and handling of the foreign keys.d
* The abstracted database layer is easier to migrate to another database system.

### CLI App
The app is structured in 3 Python files:
* **cli.py:** contains all commands defined in individual functions.
* **database.py:** contains a class that encapsulates all the code interacting with the database. Enables modularity and reusability making maintenance easier.
* **utils.py:** contains all utility functions that support the app (e.g. fetch user data from the API).

### Next features
1. Adding a timezone table
A timezone table can be added since the data is available in the API. This data could be added as a new table connected to locations, considering that multiple locations could share the same timezone.

2. Use of templates
To improve maintenance and readability templates could be used, e.g. Jinja could be incorporated (highly flexible templates). At the current level of complexity python is enough to generate simple templates, lists or dynamic SQL code.