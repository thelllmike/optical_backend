# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# # Synchronous DATABASE URL (unchanged)
# DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/optical_system"

# # Asynchronous DATABASE URL (adjust protocol as necessary for async compatibility)
# ASYNC_DATABASE_URL = "mysql+aiomysql://root:1234@localhost:3306/optical_system"

# # Existing synchronous engine (unchanged)
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # New asynchronous engine
# async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# # Asynchronous session factory
# AsyncSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=async_engine,
#     class_=AsyncSession
# )





