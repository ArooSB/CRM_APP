from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
""" 
db: SQLAlchemy

An instance of the SQLAlchemy class, used to interact with the database.

This instance will be used throughout the application to define database models, perform queries, 
and manage database connections. It provides a high-level abstraction over SQL and allows 
for easy integration with Flask applications.
"""
