from pydantic import BaseModel, validator
from typing import Optional
import logging
import datetime
from validation_logging import logging_config
from flask import Flask, flash
logger = logging_config.logger

ERROR_DICTIONARY = {
                    "Author name, 422": "invalid author name, first letter was not a capital",
                    "Author already exists, 403": "tried to add new author but author already in database",
                    "invalid birth input, 400": "probalby entered correct date however did not use / and used something else",
                    "404 author update":"data already exists in the database and user tried to upate",
                    "404, not found in userbase":"some type of search took place and data was not found in datbase"
                    }



class AuthorInput(BaseModel):
    author_name: str
    birth: str
    author_id: str 

    @validator("author_name")
    def Author_input_validate(cls,value):
        if not value[0].isupper():
            flash("<h1>first letter needs to be capital</h1>")
            logger.error(ERROR_DICTIONARY["Author name, 422"])
            raise ValueError("did not start with capital letter")
        
        else:
            logger.info("user passes through first validation check")
            return value

    @validator("author_name")
    def IsIntiger(cls,data):
        try:
            int(data)
            logger.error("invalid input, put just numbers in the author name")
            raise ValueError("input just numbers")
        
        except ValueError:
            return data

    @validator("birth")
    def Birth_input_validate(cls, data):
        valid_format = ["%d/%m/%Y","%d-%m-%Y","%d.%m.%Y"]
        for x in valid_format:
            try:
                datetime.datetime.strptime(data, x)
                logger.info(f"valid input, checked and corrected {data}")
                return data
            except ValueError:
                continue
            
        logger.error(f"{ERROR_DICTIONARY['invalid birth input']}, {data}")
        raise ValueError(f"{ERROR_DICTIONARY['invalid birth input']}, {data}")
    
        

class BookInput(BaseModel):
    book_id: str
    book_name: str

    @validator("book_name")
    def book_name_input(cls, data):
        if not data[0].isupper():
            logger.error("first letter was not an upper case")
            raise ValueError("invalid input, first letter needs to be capital")
        else:
            return data

    @validator("book_name")
    def is_intiger(cls,data):
        try:
            int(data)
            logger.error("inputted data was just numbers")
            raise ValueError("invalid input")
        except:
            return data
    
    @validator("book_id")
    def is_length(cls,data):
        if len(data) >50:
            raise ValueError("input message as too long to store in database ")
        return data

class ReviewInput(BaseModel):
    review_id: str
    review_value: str
    book_id: str

    @validator("review_value")
    def book_name_input(cls, data):
        if not data[0].isupper():
            logger.error("first letter was not an upper case")
            raise ValueError("invalid input, first letter needs to be capital")
        else:
            return data

    @validator("review_value")
    def is_length(cls,data):
        if len(data) >100:
            raise ValueError("input message as too long to store in database ")
        return data