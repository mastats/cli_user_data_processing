from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Location, Login, Picture

class UserDatabase:
    def __init__(self, db_file='sqlite:///users.db'):
        self.engine = create_engine(db_file)
        Base.metadata.create_all(self.engine)  # Create tables
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_users(self, users):
        """Inserts users into the database."""
        for user_data in users:
            user = User(
                first_name=user_data['first_name'], 
                last_name=user_data['last_name'], 
                gender=user_data['gender'], 
                email=user_data['email'], 
                phone=user_data['phone'], 
                cell=user_data['cell'],
                date_of_birth=user_data['date_of_birth'],
                age=user_data['age']
            )
            self.session.add(user)
            self.session.commit()  # Save user to get the user_id
            
            location = Location(
                user_id=user.user_id,
                street_name=user_data['street_name'], 
                street_number=user_data['street_number'], 
                city=user_data['city'],
                state=user_data['state'],
                country=user_data['country'],
                postcode=user_data['postcode'],
                latitude=user_data['latitude'],
                longitude=user_data['longitude']
            )
            login = Login(
                user_id=user.user_id,
                uuid=user_data['uuid'],
                username=user_data['username'],
                password=user_data['password'],
                salt=user_data['salt'],
                md5=user_data['md5'],
                sha1=user_data['sha1'],
                sha256=user_data['sha256']
            )
            picture = Picture(
                user_id=user.user_id,
                large=user_data['large'],
                medium=user_data['medium'],
                thumbnail=user_data['thumbnail']
            )
            
            self.session.add(location)
            self.session.add(login)
            self.session.add(picture)
        self.session.commit()

    def get_all_users(self):
        """Fetches all users from the database."""
        users = self.session.query(User).all()
        return users  # You can convert this to a list of dicts if needed

    def get_filtered_users(self, first_name=None, last_name=None, age=None, country=None):
        """Fetches filtered users based on first and last name."""
        query = self.session.query(User).join(Location)
        
        if first_name:
            query = query.filter(User.first_name.like(f'%{first_name}%'))
        if last_name:
            query = query.filter(User.last_name.like(f'%{last_name}%'))
        if age:
            query = query.filter(User.age.like(f'%{age}%'))
        if country:
            query = query.filter(Location.country.like(f'%{country}%'))

        return query.all()

    def get_users_pictures(self, size=None):
        """Fetches all users' profile images from the database."""
        if size:
            pictures = self.session.query(Picture.user_id, getattr(Picture, size)).all()
        else:
            pictures = self.session.query(Picture).all()
        return pictures