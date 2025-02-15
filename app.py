from flask import Flask, request, redirect, render_template
from google.cloud import firestore
import random
import string
import logging

# Initialize Flask app instance
app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client()

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

def generate_short_code(length=6):
    """Generate a random short URL code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get("url")
        custom_code = request.form.get("custom_code").strip()

        if not long_url:
            return render_template('index.html', error="Please enter a URL")

        # Check if the URL already exists in Firestore
        existing_doc = db.collection('urls').where('long_url', '==', long_url).get()
        
        if existing_doc:
            # If the URL exists, return the existing shortcode
            short_code = existing_doc[0].id
            short_url = request.host_url + short_code
            logging.debug(f"URL exists. Returning existing shortcode: {short_code} → {long_url}")
            return render_template('index.html', short_url=short_url)

        # If the URL doesn't exist, generate a new shortcode
        short_code = custom_code if custom_code else generate_short_code()

        # Check if the short code already exists (to avoid duplication)
        doc_ref = db.collection('urls').document(short_code)
        if doc_ref.get().exists:
            return render_template('index.html', error="Shortcode already taken")

        # Store the new URL and shortcode in Firestore
        doc_ref.set({'long_url': long_url})
        short_url = request.host_url + short_code
        logging.debug(f"Saving: {short_code} → {long_url}")
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_url(short_code):
    doc_ref = db.collection('urls').document(short_code)
    doc = doc_ref.get()

    if not doc.exists:
        return render_template('index.html', error="Short URL not found")

    long_url = doc.to_dict()['long_url']
    return redirect(long_url)

if __name__ == '__main__':
    app.run(debug=True)
