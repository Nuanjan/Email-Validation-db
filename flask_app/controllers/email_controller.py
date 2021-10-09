from flask_app import app
from flask import redirect, render_template, request, flash
from flask_app.models.email import Email


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_email', methods=['POST'])
def add_email():
    print(request.form, " this is form request")
    if not Email.validate_email(request.form):
        return redirect('/')
    data = {
        "email": request.form['e_mail']
    }
    email_id = Email.add_email(data)
    return redirect(f'email/{email_id}')


@app.route('/email/<int:email_id>')
def show_email(email_id):
    data = {
        "id": email_id
    }
    one_email = Email.get_email_by_id(data)
    flash(
        f"The email address you enterd ({one_email.email}) is a VALID email address! Thank you!", "email_success")
    all_emails = Email.all_emails()
    return render_template('email.html', all_emails=all_emails)


@app.route('/delete/<int:email_id>')
def delete_email(email_id):
    data = {
        "id": email_id
    }
    Email.delete_email_by_id(data)
    all_emails = Email.all_emails()
    return render_template('email.html', all_emails=all_emails)
