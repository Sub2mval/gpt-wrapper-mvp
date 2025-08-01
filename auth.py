# auth.py

"""
This module contains the hardcoded user authentication data.
In a real-world application, this would be replaced with a secure database
and password hashing.
"""

USERS = {
    "marketing_user": {
        "password": "marketing_password",
        "client": "marketing"
    },
    "recruiting_user": {
        "password": "recruiting_password",
        "client": "recruiting"
    }
}