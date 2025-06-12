from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Email configuration (Ethereal)
app.config.update(
    MAIL_SERVER='smtp.ethereal.email',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='herbert.romaguera@ethereal.email',
    MAIL_PASSWORD='w1GwUTnxW1uRNXx2GW',
    MAIL_DEFAULT_SENDER='herbert.romaguera@ethereal.email'
)

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/option2')
def option2():
    return render_template('index2.html')

@app.route('/option3')
def option3():
    return render_template('index3.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/showroom', methods=['GET', 'POST'])
def showroom():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        location = request.form.get('location')
        message = request.form.get('message')

        msg = Message("New Showroom Appointment", recipients=['herbert.romaguera@ethereal.email'])
        msg.body = f"""Showroom Booking Request:
Name: {name}
Email: {email}
Preferred Date: {date}
Location: {location}
Message: {message}
"""
        mail.send(msg)
        flash("Appointment request submitted successfully.")
        return redirect(url_for('showroom'))

    return render_template('showroom.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        form_type = request.form.get('form_type')

        if form_type == 'quote':
            phone = request.form.get('phone')
            interest = request.form.get('interest')
            message = request.form.get('message')

            msg = Message("New Quotation Request", recipients=['herbert.romaguera@ethereal.email'])
            msg.body = f"""Quotation Request:
Name: {name}
Email: {email}
Phone: {phone}
Interests: {interest}
Message: {message}
"""

        else:  # 'product'
            category = request.form.get('category')
            product_code = request.form.get('product_code')
            product_message = request.form.get('product_message')

            msg = Message("Product Price Inquiry", recipients=['herbert.romaguera@ethereal.email'])
            msg.body = f"""Product Inquiry:
Name: {name}
Email: {email}
Category: {category}
Product Description: {product_code}
Message: {product_message}
"""

        mail.send(msg)
        flash("Thank you for contacting us!")
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
