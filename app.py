from flask import Flask, request, redirect, url_for, render_template, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os



app = Flask(__name__)

# Pricing data
pricing_data = {
    "TATA/Waaree": {
        "1 KW": {"total": 86000, "subsidy": 30300, "meter": 2500, "after_subsidy": 55700},
        "2 KW": {"total": 148000, "subsidy": 60000, "meter": 2500, "after_subsidy": 88000},
        "3 KW": {"total": 215000, "subsidy": 78000, "meter": 2500, "after_subsidy": 137000},
        "4 KW": {"total": 265000, "subsidy": 78000, "meter": 2500, "after_subsidy": 187000},
        "5 KW": {"total": 330000, "subsidy": 78000, "meter": 2500, "after_subsidy": 252000},
        "6 KW": {"total": 395000, "subsidy": 78000, "meter": 2500, "after_subsidy": 317000},
        "7 KW": {"total": 452000, "subsidy": 78000, "meter": 2500, "after_subsidy": 374000},
        "8 KW": {"total": 525000, "subsidy": 78000, "meter": 2500, "after_subsidy": 447000},
        "9 KW": {"total": 589000, "subsidy": 78000, "meter": 2500, "after_subsidy": 511000},
        "10 KW": {"total": 649000, "subsidy": 78000, "meter": 2500, "after_subsidy": 571000}
    },
    "Adani": {
        "1 KW": {"total": 86000, "subsidy": 30300, "meter": 2500, "after_subsidy": 55700},
        "2 KW": {"total": 148000, "subsidy": 60000, "meter": 2500, "after_subsidy": 88000},
        "3 KW": {"total": 212000, "subsidy": 78000, "meter": 2500, "after_subsidy": 134000},
        "4 KW": {"total": 261000, "subsidy": 78000, "meter": 2500, "after_subsidy": 183000},
        "5 KW": {"total": 323000, "subsidy": 78000, "meter": 2500, "after_subsidy": 247000},
        "6 KW": {"total": 393000, "subsidy": 78000, "meter": 2500, "after_subsidy": 315000},
        "7 KW": {"total": 448000, "subsidy": 78000, "meter": 2500, "after_subsidy": 370000},
        "8 KW": {"total": 524000, "subsidy": 78000, "meter": 2500, "after_subsidy": 442000},
        "9 KW": {"total": 584000, "subsidy": 78000, "meter": 2500, "after_subsidy": 506000},
        "10 KW": {"total": 649000, "subsidy": 78000, "meter": 2500, "after_subsidy": 571000}
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-cost', methods=['POST'])
def send_cost():
    try:
        name = request.form['name']
        email = request.form['email']
        capacity = request.form['capacity']

        tata_waaree = pricing_data["TATA/Waaree"][capacity]
        adani = pricing_data["Adani"][capacity]

        # --- Generate PDF ---
        pdf_path = os.path.join(os.getcwd(), f"{name.replace(' ', '_')}_quote.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Title and customer info
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, f"Rubix Solar Energy - Quote for {capacity}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Customer Name: {name}")
        
        # TATA/Waaree pricing
        c.drawString(50, 700, f"TATA/Waaree:")
        c.drawString(70, 680, f"Total Price: ₹{tata_waaree['total']}")
        c.drawString(70, 660, f"Subsidy: ₹{tata_waaree['subsidy']}")
        c.drawString(70, 640, f"Meter Charges: ₹{tata_waaree['meter']}")
        c.drawString(70, 620, f"Price After Subsidy: ₹{tata_waaree['after_subsidy']}")

        # Adani pricing
        c.drawString(50, 590, f"Adani:")
        c.drawString(70, 570, f"Total Price: ₹{adani['total']}")
        c.drawString(70, 550, f"Subsidy: ₹{adani['subsidy']}")
        c.drawString(70, 530, f"Meter Charges: ₹{adani['meter']}")
        c.drawString(70, 510, f"Price After Subsidy: ₹{adani['after_subsidy']}")

        # Contact information
        c.drawString(50, 480, f"For queries, contact: 8520087081 / rubixenergysystems@gmail.com")
        
        # Important notice
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 450, "IMPORTANT NOTICE:")
        c.setFont("Helvetica", 10)
        c.drawString(50, 430, "* This is a system-generated quotation for reference purposes only.")
        c.drawString(50, 410, "* Prices may increase or decrease based on market conditions.")
        c.drawString(50, 390, "* Final pricing will be confirmed at the time of purchase agreement.")
        c.drawString(50, 370, "* Government subsidies are subject to approval and availability.")
        c.drawString(50, 350, "* This quote is valid for 7 days from the date of generation.")
        
        c.save()

        # Update email body with pricing and alert message
        body = f"""
        Dear {name},

        Thank you for your interest in Rubix Solar Energy solutions. Please find attached your customized quote for a {capacity} solar system.

        Quick Summary:
        --------------
        TATA/Waaree System:
        - Total Price: ₹{tata_waaree['total']}
        - Price After Subsidy: ₹{tata_waaree['after_subsidy']}

        Adani System:
        - Total Price: ₹{adani['total']}
        - Price After Subsidy: ₹{adani['after_subsidy']}

        Important Notice:
        ----------------
        * This is a system-generated quotation for reference purposes only
        * Prices may increase or decrease based on market conditions
        * Final pricing will be confirmed at the time of purchase agreement
        * Government subsidies are subject to approval and availability
        * This quote is valid for 7 days from the date of generation

        For any queries or to proceed with installation, please contact us at:
        Phone: 8520087081
        Email: rubixenergysystems@gmail.com

        Regards,
        Rubix Solar Energy Team
        """

        # Define sender email and password
        sender_email = "ginjupallysainikhil@gmail.com"
        sender_password = "kpvj qwxv uxhs pajl"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"Quote for {capacity} Solar System"

        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open(pdf_path, "rb") as f:
            part = MIMEText(f.read(), 'base64', 'utf-8')
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
            part.add_header('Content-Type', 'application/pdf; name="quote.pdf"')
            msg.attach(part)

        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Email error: {e}")

        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        return jsonify({
            'status': 'success',
            'message': 'Quote sent successfully! Please check your email.'
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Error sending quote. Please try again.'
        }), 500
@app.route('/subscribe', methods=['POST'])
def subscribe():
    full_name = request.form['full_name']
    email = request.form['email']

    # Email to the subscriber
    email_body = f"""
    Dear {full_name},

    Thank you for subscribing to the Rubix Solar Energy newsletter! You'll receive updates on the latest solar panel technologies and offers.

    Subscription Details:
    Full Name: {full_name}
    Email: {email}

    Best regards,
    Rubix Solar Energy Team
    Contact: 8520087081 | rubixenergysystems@gmail.com
    """

    # Email setup
    sender_email = "ginjupallysainikhil@gmail.com"
    sender_password = "kpvj qwxv uxhs pajl"
    owner_email = "ginjupallysainikhil@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['CC'] = owner_email
    msg['Subject'] = "Welcome to Rubix Solar Energy Newsletter"
    msg.attach(MIMEText(email_body, 'plain'))

    # Combine recipient and CC for sending
    recipients = [email, owner_email]

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")
        return redirect(url_for('index') + '#contact?status=error')

    return redirect(url_for('index') + '#contact?status=success')

@app.route('/contact', methods=['POST'])
def contact():
    full_name = request.form['full_name']
    contact_number = request.form['contact_number']
    email = request.form['email']
    message = request.form['message']


    # Email to the SMTP owner (your team)
    smtp_body = f"""
    New Contact Form Submission:

    Someone wants to contact Rubix Solar Energy Team!

    Details:
    Full Name: {full_name}
    Contact Number: {contact_number}
    Email: {email}
    Message: {message}

    Best regards,
    Rubix Solar Contact System
    """

    # Auto-reply to the person who submitted the form
    auto_reply_body = f"""
    Dear {full_name},

    Thank you for contacting Rubix Solar Energy!

    We have received your message and our team will get back to you shortly.

    Your submitted details:
    Name: {full_name}
    Contact: {contact_number}
    Email: {email}
    Message: {message}

    Best regards,
    Rubix Solar Energy Team
    Contact: 8520087081
    Email: rubixenergysystems@gmail.com
    """

    try:
        # Setup SMTP
        sender_email = "ginjupallysainikhil@gmail.com"
        sender_password = "kpvj qwxv uxhs pajl"
        smtp_owner_email = "ginjupallysainikhil@gmail.com"

        # Send email to SMTP owner
        msg_to_owner = MIMEMultipart()
        msg_to_owner['From'] = sender_email
        msg_to_owner['To'] = smtp_owner_email
        msg_to_owner['Subject'] = "New Contact Form Submission - Rubix Solar"
        msg_to_owner.attach(MIMEText(smtp_body, 'plain'))

        # Send auto-reply to customer
        msg_to_customer = MIMEMultipart()
        msg_to_customer['From'] = sender_email
        msg_to_customer['To'] = email
        msg_to_customer['Subject'] = "Thank you for contacting Rubix Solar Energy"
        msg_to_customer.attach(MIMEText(auto_reply_body, 'plain'))

        # Connect to SMTP server and send both emails
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send to owner
        server.send_message(msg_to_owner)
        # Send to customer
        server.send_message(msg_to_customer)
        
        server.quit()
        
        return jsonify({
            'status': 'success',
            'message': 'Your message has been sent successfully! We will contact you soon.'
        })

    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Sorry, there was an error sending your message. Please try again.'
        })

if __name__ == '__main__':
    app.run(debug=True)