# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Update these variables with your actual credentials
# username = 'thellmike'
# password = '1080%40%23Mike'  # Encoded password
# server = 'opsbackend.mysql.database.azure.com'
# database_name = 'optical_system'  # Change to your database name

# DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{server}/{database_name}"

# engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` is optional, for debugging purposes
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


