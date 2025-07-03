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
    max_date = (datetime.today() + timedelta(days=180)).strftime('%Y-%m-%d')  # 6 months (180 days) from today
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

        # Format the date for display (convert from YYYY-MM-DD to DD/MM/YYYY)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d/%m/%Y')
        except:
            formatted_date = date  # fallback to original if parsing fails

        # Format the time for display (convert 24hr to 12hr with AM/PM)
        try:
            time_obj = datetime.strptime(time, '%H:%M')
            formatted_time = time_obj.strftime('%I:%M %p')
        except:
            formatted_time = time  # fallback to original if parsing fails

        msg = Message("🗓️ New Meeting Request - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
        msg.body = f"""MEETING BOOKING REQUEST
{"="*50}

📋 CLIENT DETAILS:
Name: {name}
Email: {email}
Phone: {phone}

📅 MEETING DETAILS:
Preferred Date: {formatted_date}
Preferred Time: {formatted_time}
Meeting Location: {location}

📝 PROJECT INFORMATION:
{message if message else 'No additional details provided'}

---
⚠️  ACTION REQUIRED: Please contact the client within 24 hours to confirm meeting details.

📧 Reply to: {email}
📱 Call/WhatsApp: {phone}

Sent from: Uniglobe Lifestyles Website - Meeting Booking Form
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
        try:
            print("=== MEETING BOOKING EMAIL ===")
            print(f"Subject: {msg.subject}")
            print(f"Recipients: {msg.recipients}")
            print("Body:")
            print(msg.body)
            print("=" * 50)
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
        company = request.form.get('company')
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
{f"Company: {company}" if company else "Company: Individual/Not specified"}
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
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
        try:
            print("=== QUOTATION EMAIL ===")
            print(f"Subject: {msg.subject}")
            print(f"Recipients: {msg.recipients}")
            print("Body:")
            print(msg.body)
            print("=" * 50)
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
        product_desc = request.form.get('product_desc')  # This will come from hidden input
        message = request.form.get('message')

        if not name or not email:
            flash("Name and email are required.", "danger")
            return redirect(url_for('product_pricing'))

        # Check if this is a wishlist request
        is_wishlist = category == 'My Wishlist'
        is_all_wishlist = product_desc and 'ALL WISHLIST ITEMS:' in product_desc
        is_single_wishlist = product_desc and 'WISHLIST ITEM:' in product_desc
        
        if is_wishlist:
            if is_all_wishlist:
                # All wishlist items request
                msg = Message("🤍 Complete Wishlist Pricing - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
                msg.body = f"""COMPLETE WISHLIST PRICING REQUEST
{"="*65}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

🤍 COMPLETE WISHLIST REQUEST:
The client wants pricing for ALL items in their wishlist.

📝 ALL WISHLIST ITEMS:
{product_desc.replace('ALL WISHLIST ITEMS:', '').strip() if product_desc else 'Items not properly loaded'}

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: 
- Provide comprehensive pricing for ALL wishlist items
- Include bulk discount options (10+ items)
- Consider package deals for multiple categories
- Respond within 1 business day

� Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Complete Wishlist Pricing
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
            elif is_single_wishlist:
                # Single wishlist item request
                selected_item = product_desc.replace('WISHLIST ITEM:', '').strip()
                msg = Message("🤍 Wishlist Item Pricing - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
                msg.body = f"""WISHLIST ITEM PRICING REQUEST
{"="*60}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

🤍 SPECIFIC WISHLIST ITEM:
Product Code: {selected_item}
(Selected from client's wishlist)

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: 
- Provide detailed pricing for the selected item
- Include quantity-based pricing if applicable
- Suggest related products from their wishlist
- Respond within 1 business day

📧 Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Wishlist Item Pricing
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
            else:
                # Fallback for other wishlist cases
                msg = Message("🤍 Wishlist Price Inquiry - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
                msg.body = f"""WISHLIST PRICE INQUIRY
{"="*60}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

🤍 WISHLIST REQUEST:
{product_desc if product_desc else 'Wishlist items not properly loaded'}

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: Please provide pricing for the requested wishlist items within 1 business day.

📧 Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Wishlist Pricing Request
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
        else:
            # Regular product inquiry
            is_general_inquiry = product_desc and 'General inquiry for' in product_desc
            
            if is_general_inquiry:
                # Category-wide inquiry
                msg = Message("📋 Category Pricing Inquiry - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
                msg.body = f"""CATEGORY PRICING INQUIRY
{"="*55}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

📋 CATEGORY INQUIRY:
{product_desc}

The client is interested in general pricing information for this entire category.

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: 
- Provide category overview with price ranges
- Include popular items in this category
- Suggest bestsellers and featured products
- Respond within 1 business day

📧 Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Category Pricing Inquiry
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
            else:
                # Specific product inquiry
                msg = Message("🏷️ Product Price Inquiry - Uniglobe Lifestyles", recipients=['uniglobelifestyles@gmail.com'])
                msg.body = f"""PRODUCT PRICE INQUIRY
{"="*50}

👤 CLIENT DETAILS:
Name: {name}
Email: {email}

🛋️ PRODUCT INFORMATION:
Category: {category if category else 'Not specified'}
Product Code/Description: {product_desc if product_desc else 'Not provided'}

📝 ADDITIONAL REQUIREMENTS:
{message if message else 'No additional information provided'}

---
⚠️  ACTION REQUIRED: Please provide product pricing and availability within 1 business day.

📧 Reply to: {email}

Sent from: Uniglobe Lifestyles Website - Product Pricing Form
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
        try:
            print("=== PRODUCT PRICING EMAIL ===")
            print(f"Subject: {msg.subject}")
            print(f"Recipients: {msg.recipients}")
            print("Body:")
            print(msg.body)
            print("=" * 50)
            mail.send(msg)
            if is_wishlist:
                if is_all_wishlist:
                    flash("Complete wishlist pricing request submitted! We'll send you detailed pricing for all your wishlist items with bulk discounts.", "success")
                elif is_single_wishlist:
                    flash("Wishlist item pricing request submitted! We'll send you detailed pricing for the selected item.", "success")
                else:
                    flash("Wishlist pricing request submitted successfully!", "success")
            elif product_desc and 'General inquiry for' in product_desc:
                flash("Category pricing inquiry submitted! We'll send you comprehensive information about this category.", "success")
            else:
                flash("Product pricing request submitted successfully!", "success")
        except Exception as e:
            print("Error sending mail:", e)
            flash("Failed to send request. Please try again.", "danger")

        return redirect(url_for('product_pricing'))

    return render_template('product_pricing_form.html')

@app.route('/test-emails')
def test_emails():
    """Test route to preview all email templates"""
    from datetime import datetime, timedelta
    
    # Test data
    test_data = {
        'name': 'John Doe',
        'company': 'ABC Architecture Firm',
        'email': 'john@example.com',
        'phone': '+91 9876543210',
        'date': '2025-07-10',
        'time': '14:00',
        'location': 'Mumbai Office, Andheri West',
        'message': 'Looking for furniture for 3BHK apartment',
        'project': 'Residential Interior Design',
        'category': 'Bedroom & Beds',
        'product_desc': 'BD15'
    }
    
    # Format date and time
    date_obj = datetime.strptime(test_data['date'], '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    time_obj = datetime.strptime(test_data['time'], '%H:%M')
    formatted_time = time_obj.strftime('%I:%M %p')
    
    emails = []
    
    # 1. Meeting Booking Email
    meeting_email = f"""MEETING BOOKING REQUEST
{"="*50}

📋 CLIENT DETAILS:
Name: {test_data['name']}
Email: {test_data['email']}
Phone: {test_data['phone']}

📅 MEETING DETAILS:
Preferred Date: {formatted_date}
Preferred Time: {formatted_time}
Meeting Location: {test_data['location']}

📝 PROJECT INFORMATION:
{test_data['message']}

---
⚠️  ACTION REQUIRED: Please contact the client within 24 hours to confirm meeting details.

📧 Reply to: {test_data['email']}
📱 Call/WhatsApp: {test_data['phone']}

Sent from: Uniglobe Lifestyles Website - Meeting Booking Form
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
    
    emails.append(("🗓️ New Meeting Request - Uniglobe Lifestyles", meeting_email))
    
    # 2. Quotation Email
    quotation_email = f"""QUOTATION REQUEST
{"="*50}

👤 CLIENT DETAILS:
Name: {test_data['name']}
Company: {test_data['company']}
Email: {test_data['email']}
Phone: {test_data['phone']}

🏗️ PROJECT INFORMATION:
Project Type/Products: {test_data['project']}

📝 ADDITIONAL DETAILS:
{test_data['message']}

---
⚠️  ACTION REQUIRED: Please prepare and send quotation within 2 business days.

📧 Reply to: {test_data['email']}
📱 Contact: {test_data['phone']}

Sent from: Uniglobe Lifestyles Website - Quotation Request Form
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
    
    emails.append(("💰 New Quotation Request - Uniglobe Lifestyles", quotation_email))
    
    # 3. Product Pricing Email
    product_email = f"""PRODUCT PRICE INQUIRY
{"="*50}

👤 CLIENT DETAILS:
Name: {test_data['name']}
Email: {test_data['email']}

🛋️ PRODUCT INFORMATION:
Category: {test_data['category']}
Product Code/Description: {test_data['product_desc']}

📝 ADDITIONAL REQUIREMENTS:
{test_data['message']}

---
⚠️  ACTION REQUIRED: Please provide product pricing and availability within 1 business day.

📧 Reply to: {test_data['email']}

Sent from: Uniglobe Lifestyles Website - Product Pricing Form
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
    
    emails.append(("🏷️ Product Price Inquiry - Uniglobe Lifestyles", product_email))
    
    # 4. Wishlist Email (All Items)
    wishlist_all = """ALL WISHLIST ITEMS:
1. BD15 - bedroom
2. LV8 - living
3. DG12 - dining
"""
    
    wishlist_email = f"""COMPLETE WISHLIST PRICING REQUEST
{"="*65}

👤 CLIENT DETAILS:
Name: {test_data['name']}
Email: {test_data['email']}

🤍 COMPLETE WISHLIST REQUEST:
The client wants pricing for ALL items in their wishlist.

📝 ALL WISHLIST ITEMS:
{wishlist_all.strip()}

📝 ADDITIONAL REQUIREMENTS:
{test_data['message']}

---
⚠️  ACTION REQUIRED: 
- Provide comprehensive pricing for ALL wishlist items
- Include bulk discount options (10+ items)
- Consider package deals for multiple categories
- Respond within 1 business day

📧 Reply to: {test_data['email']}

Sent from: Uniglobe Lifestyles Website - Complete Wishlist Pricing
Time: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}
"""
    
    emails.append(("🤍 Complete Wishlist Pricing - Uniglobe Lifestyles", wishlist_email))
    
    # Return HTML page showing all emails
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Templates Preview</title>
        <style>
            body { font-family: monospace; margin: 20px; }
            .email { border: 2px solid #ccc; margin: 20px 0; padding: 15px; background: #f9f9f9; }
            .subject { font-weight: bold; color: #0066cc; margin-bottom: 10px; }
            .body { white-space: pre-wrap; background: white; padding: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Email Templates Preview</h1>
        <p>These are the email templates that will be sent for each form:</p>
    """
    
    for subject, body in emails:
        html += f"""
        <div class="email">
            <div class="subject">Subject: {subject}</div>
            <div class="body">{body}</div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html

if __name__ == '__main__':
    app.run(debug=True)
