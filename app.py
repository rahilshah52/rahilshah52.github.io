from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
from flask import Flask, render_template

app = Flask(__name__)
# List of product categories (editable!)
categories = ['bedroom', 'living', 'dining', 'modular', 'lighting', 'sanitaryware', 'premium']
# Put this near the top or in a global config section
homepage_display = {
    'bedroom': 'images/bedroom/bed 15.webp',
    'living': 'images/living/living_room 19.webp',
    'dining': 'images/dining/tables_catalog_18_1.webp',
    'modular': 'images/modular/plywood_cabinet 17.webp',
    'lighting': 'images/lighting/lighting 1.webp',
    'sanitaryware': 'images/sanitaryware/washbasin_faucets 78.webp',
    'premium': 'images/premium/baxter_2_128_5.webp'
}
homepage_display_names = {
    'bedroom': 'Bedroom & Bed',
    'living': 'Lounge Seating',
    'dining': 'Dining & Coffee Tables',
    'modular': 'Modular Cabinets',
    'lighting': 'Lightings & Fixtures',
    'sanitaryware': 'Sanitaryware',
    'premium': 'Premium Collection',
}


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Email configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='uniglobelifestyles@gmail.com',
    MAIL_PASSWORD='gmnh dwdq hsrm bnrf',  # Consider using environment variables
    MAIL_DEFAULT_SENDER='uniglobelifestyles@gmail.com'
)

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index1.html', homepage_display=homepage_display, homepage_display_names=homepage_display_names)

@app.route('/catalogs')
def catalogs():
    return render_template('catalogs.html')

@app.route('/about')
def about():
    return render_template('about.html')

import os

@app.route('/products')
def products():
    base_path = os.path.join(app.static_folder, 'images')

    category_display_names = {
        'bedroom': 'Bedroom & Beds',
        'living': 'Sofa & Lounge Seating',
        'dining': 'Dining & Coffee Tables',
        'modular': 'Modular Furniture and Cabinets',
        'lighting': 'Lighting & Fixtures',
        'sanitaryware': 'Sanitaryware & Bathroom Fittings',
        'Premium': 'Premuim Collection'
    }

    category_prefixes = {
        'bedroom': 'BD',
        'living': 'LV',
        'dining': 'DG',
        'modular': 'MC',
        'lighting': 'LG',
        'sanitaryware': 'SW',
        'premium': 'PC'
    }

    product_images = {}

    for category, prefix in category_prefixes.items():
        folder_path = os.path.join(base_path, category)
        if os.path.isdir(folder_path):
            images = sorted(os.listdir(folder_path))
            product_images[category] = {
                'display_name': category_display_names.get(category, category.title()),
                'items': []
            }
            for i, img in enumerate(images, start=1):
                if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    code = f"{prefix}{i}"
                    product_images[category]['items'].append({
                        'filename': img,
                        'code': code
                    })

    return render_template('products.html', product_images=product_images)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/showroom', methods=['GET', 'POST'])
def showroom():
    today = datetime.today().strftime('%Y-%m-%d')  # Get today's date in proper format
    max_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')  # 30 days from today
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')  # Added time field
        location = request.form.get('location')
        message = request.form.get('message')

        if not name or not email or not date or not location or not time:  # Added time to validation
            flash("All fields marked with * are required.", "danger")
            return redirect(url_for('showroom'))

        msg = Message("New Showroom Appointment", recipients=['uniglobelifestyles@gmail.com'])
        msg.body = f"""Showroom Booking Request:
Name: {name}
Email: {email}
Preferred Date: {date}
Preferred Time: {time}
Showroom Location: {location}
Message: {message or 'No additional message'}
"""
        try:
            mail.send(msg)
            flash("Appointment request submitted successfully.", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Something went wrong while sending the email. Please try again.", "danger")

        return redirect(url_for('showroom'))

    return render_template('showroom.html', current_date=today, max_date=max_date)


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
            project = request.form.get('project')  # Fixed: was 'interest'
            message = request.form.get('message')

            msg = Message("New Quotation Request", recipients=['uniglobelifestyles@gmail.com'])
            msg.body = f"""Quotation Request:
Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Project Type: {project or 'Not specified'}
Additional Info: {message or 'None'}
"""
        else:
            category = request.form.get('category')
            product_desc = request.form.get('product_desc')  # Fixed: was 'product_code'
            message = request.form.get('message')  # Fixed: was 'product_message'

            msg = Message("Product Price Inquiry", recipients=['uniglobelifestyles@gmail.com'])
            msg.body = f"""Product Inquiry:
Name: {name}
Email: {email}
Category: {category or 'Not specified'}
Product Description: {product_desc or 'Not provided'}
Message: {message or 'None'}
"""

        try:
            mail.send(msg)
            flash("Thank you for contacting us!", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Failed to send message. Please try again.", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
