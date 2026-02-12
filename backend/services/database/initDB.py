'''
Initialize the database and create tables if they do not exist.
This module is intended to be run once during application startup.
'''

import logging
from fastapi import FastAPI
from connection import get_conn

async def initilizeDatabase(app: FastAPI):
    '''
    Initialize the database and create tables if they do not exist
    
    :param app: the FastAPI object to access the database connection pool
    :type app: FastAPI
    '''
    
    async with get_conn(app) as conn:
        with open("queries/init.sql") as file:
            conn.execute(file.read())