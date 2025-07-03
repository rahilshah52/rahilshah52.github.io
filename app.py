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
    min_date = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')  # 2 days from today (day after tomorrow)
    max_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')  # 30 days from today
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        time = request.form.get('time')  # Added time field
        location = request.form.get('location')
        message = request.form.get('message')

        if not name or not email or not phone or not date or not location or not time:  # Added phone to validation
            flash("All fields marked with * are required.", "danger")
            return redirect(url_for('showroom'))

        msg = Message("🗓️ New Meeting Request - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
        msg.body = f"""MEETING BOOKING REQUEST
{"="*50}

📋 CLIENT DETAILS:
Name: {name}
Email: {email}
Phone: {phone}

📅 MEETING DETAILS:
Preferred Date: {date}
Preferred Time: {time}
Meeting Location: {location}

📝 PROJECT INFORMATION:
{message if message else 'No additional details provided'}

---
⚠️  ACTION REQUIRED: Please contact the client within 24 hours to confirm meeting details.

📧 Reply to: {email}
📱 Call/WhatsApp: {phone}

Sent from: Uniglobe Lifestyles Website - Meeting Booking Form
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        try:
            mail.send(msg)
            flash("Meeting request submitted successfully. We'll contact you to confirm the details.", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Something went wrong while sending the email. Please try again.", "danger")

        return redirect(url_for('showroom'))

    return render_template('showroom.html', current_date=today, min_date=min_date, max_date=max_date)


@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    # Check if there's a form parameter to show specific forms
    form_type = request.args.get('form')
    if form_type == 'product':
        return redirect(url_for('product_pricing'))
    elif form_type == 'quote':
        return redirect(url_for('quotation'))
    
    return render_template('contact_new.html')

@app.route('/quotation', methods=['GET', 'POST'])
def quotation():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        project = request.form.get('project')
        message = request.form.get('message')

        if not name or not email:
            flash("Name and email are required.", "danger")
            return redirect(url_for('quotation'))

        msg = Message("💰 New Quotation Request - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
        msg.body = f"""QUOTATION REQUEST
{"="*50}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}

🏗️ PROJECT INFORMATION:
Project Type/Products: {project if project else 'Not specified'}

📝 ADDITIONAL DETAILS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: Please prepare and send quotation within 2 business days.

📧 Reply to: {email}
📱 Contact: {phone if phone else 'Email only'}

Sent from: Uniglobe Lifestyles Website - Quotation Request Form
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        try:
            mail.send(msg)
            flash("Quotation request submitted successfully!", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Failed to send request. Please try again.", "danger")

        return redirect(url_for('quotation'))

    return render_template('quotation_form.html')

@app.route('/product-pricing', methods=['GET', 'POST'])
def product_pricing():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        category = request.form.get('category')
        product_desc = request.form.get('product_desc')
        message = request.form.get('message')

        if not name or not email:
            flash("Name and email are required.", "danger")
            return redirect(url_for('product_pricing'))

        msg = Message("🏷️ Product Price Inquiry - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
        msg.body = f"""PRODUCT PRICE INQUIRY
{"="*50}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

🛋️ PRODUCT INFORMATION:
Category: {category if category else 'Not specified'}
Product Description/Code: {product_desc if product_desc else 'Not provided'}

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: Please provide product pricing and availability within 1 business day.

📧 Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Product Pricing Form
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        try:
            mail.send(msg)
            flash("Product pricing request submitted successfully!", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Failed to send request. Please try again.", "danger")

        return redirect(url_for('product_pricing'))

    return render_template('product_pricing_form.html')

if __name__ == '__main__':
    app.run(debug=True)
