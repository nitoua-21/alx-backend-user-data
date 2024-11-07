#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import re
import logging
import mysql.connector
import os
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replaces sensitive information in a message with redaction string

    Args:
        fields: List of strings representing fields to obfuscate
        redaction: String to replace sensitive information with
        message: String containing sensitive data
        separator: String separator for fields in message

    Returns:
        String with sensitive information replaced by redaction
    """
    for field in fields:
        pattern = f'(?<=){field}=.*?{separator}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log records and redact sensitive information
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger for handling personal data

    Returns:
        logging.Logger: Configured logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to the database

    Returns:
        MySQLConnection: Database connection object
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """Main function to retrieve and display filtered user data"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()
    fields = cursor.column_names

    for row in cursor:
        message = "".join(f"{fields[i]}={str(row[i])}; "
                          for i in range(len(fields)))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
