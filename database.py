# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# database.py
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# # Update the DATABASE_URL to use aiomysql
# DATABASE_URL = "mysql+aiomysql://root:1234@localhost:3306/optical_system"

# engine = create_async_engine(DATABASE_URL)
# AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


