# CLI to fetch user data
CLI app that interacts with an external API to fetch user data (https://randomuser.me/api/).
An additional API is used to fetch weather data for each user location (https://open-meteo.com/en/docs#current=temperature_2m&hourly=).
This app is tested in the following Python versions: 3.9.6, 3.10.

## Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/mastats/cli_user_data_processing.git
cd random_user_cli
```

2. **Install Dependencies:**

Install the dependencies in the requirements file (Requests & Click)
```bash 
pip install -r requirements.txt
```

3. **Run the CLI:**

Run the CLI app an checkout the --help for a list of available commands.
```bash
python cli.py --help
```
## Commands

1. **Import Users:**

Fetch and import users from the API into the database. You can use the --results argument to define how many users are to be fetched.
```bash
python cli.py import-users --results 100
```

2. **Export Users:**

Exports all users to a CSV file. You can use the --file argument to set the name of the output file.
```bash
python cli.py export-users --file users.csv
```

3. **Show Users:**

Show all users or filter by first name, last name.
```bash
python cli.py show-users --first_name John --last_name Doe
```

4. **Download Images:**

Download all user profile images to a local directory. You can use the --dir argument to set the name of the directory. The app will create the necessary folders for you.
In order to facilitate the download of a large volume of pictures in an efficient way, this task is executed with async functions.
```bash
python cli.py download-images --dir ./images
```

## Containerization

You can also run this solution from a container. Check the Dockerfile included in this repository to build the image and run it from your laptop of preferred Docker service.

1. **Build the Docker image:**

```bash
docker build -t random_user_cli .
```

2. **Start the container:**

```bash
docker run -it random_user_cli
```

2. **Run the CLI app inside the container:**

If you are inside the container then:

```bash
python cli.py import-users --results 10
```

If you only want to execute a specific task then:

```bash
docker run random_user_cli python cli.py import-users --results 100
```

## Design & asumptions

### Data model

All the fetched data is structured and stored in a normalized way by using the following tables:

1. **Users**
2. **Locations.**
3. **Logins**
4. **IDs**
5. **Pictures**

Design key points:

* The main table is **users** and all other tables have user_id as a foreign key. This allows for a natural flow of information where the user information should come first and then locations, logins, pictures or any other data tied to each user. 
* This model reduces redundancy since each table stores distinct data, solves partial dependencies and makes data updates flexible.
* Transactional inserts to commit each user in batches are used to improve performance, ensure atomicity and correct handle of the foreign keys.
* The abstracted database layer is easier to migrate to another database system.
* SQLAlchemy is used for the multiple benefits it offers like:
    * Abstract the database engine allowing to work with multiple databases with minimal changes.
    * Write less raw queries (E.g. filter_by).
    * Data validation and integrity checks

### CLI App

The app is structured in 3 Python files:

* **cli.py:** contains all commands defined in individual functions.
* **database.py:** contains a class that encapsulates all the code interacting with the database. Enables modularity and reusability making maintenance easier.
* **models.py** contains the model definition with the tables structure focusing on normalized storage. Expected data types are enforced by SQLAlchemy.
* **utils.py:** contains all utility functions that support the app (e.g. fetch user data from the API).

### Next features and improvements

1. **Adding a timezone table**

A timezone table can be added since the data is available in the API. This data could be added as a new table connected to locations, considering that multiple locations could share the same timezone.

2. **Use of templates**

To improve maintenance and readability templates could be used, e.g. Jinja could be incorporated (highly flexible templates). At the current level of complexity python is enough to generate simple templates, lists or dynamic SQL code.

3. **Use of classes for the CLI app**

As the app grows and becomes more complex the uses of classes can be beneficial. Specially if there are commands that share logic or need to be grouped, additional modularity, configuration or session data is required. 

4. **Wrap the CLI in a Web Service**

Flask or FastAPI could be used to create an HTTP interface with multiple endpoints that runs the CLI commands with the requested parameters. The web service could be accessed directly or provided as a part of a in-house backoffice solution made with any front-end framework.
