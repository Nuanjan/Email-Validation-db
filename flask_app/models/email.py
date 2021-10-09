from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Email:
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_email(emailForm):
        is_valid = True
        if not EMAIL_REGEX.match(emailForm['e_mail']):
            flash("Invalid email address!", 'email_error')
            is_valid = False
        data = {"email": emailForm['e_mail']}
        if Email.get_email_by_email(data):
            flash("Thia Email already taken!", "email_error")
            is_valid = False
        return is_valid

    @classmethod
    def all_emails(cls):
        query = "SELECT * FROM emails"
        results = connectToMySQL('email_schema').query_db(query)
        emails = []
        for email in results:
            emails.append(cls(email))
        print(emails, " this is email list from db list")
        return emails

    @classmethod
    def add_email(cls, data):
        query = "INSERT INTO emails(email, created_at, updated_at) VALUES(%(email)s, NOW(),NOW())"
        return connectToMySQL('email_schema').query_db(query, data)

    @classmethod
    def get_email_by_id(cls, data):
        query = "SELECT * FROM emails WHERE emails.id = %(id)s"
        results = connectToMySQL('email_schema').query_db(query, data)
        emails = []
        for email in results:
            emails.append(cls(email))
        return emails[0]

    @classmethod
    def get_email_by_email(cls, data):
        query = "SELECT * FROM emails WHERE email = %(email)s"
        emails = connectToMySQL('email_schema').query_db(query, data)
        if len(emails) > 0:
            return True
        return False

    @classmethod
    def delete_email_by_id(cls, data):
        query = "DELETE FROM emails WHERE emails.id = %(id)s"
        return connectToMySQL('email_schema').query_db(query, data)
