from flask import Flask, render_template, request, jsonify, send_file
import pyotp
import qrcode
import json
from pathlib import Path
from datetime import datetime
import io
import base64

app = Flask(__name__)

class MFADemo:
    def __init__(self, storage_file="/app/data/registered_devices.json"):
        self.storage_file = Path(storage_file)
        self.devices = self._load_devices()

    def _load_devices(self):
        if self.storage_file.exists():
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_devices(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.devices, f, indent=4)

    def register_device(self, username):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            username,
            issuer_name="MFA Web Demo"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Create QR code image in memory
        img_buffer = io.BytesIO()
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(img_buffer)
        img_buffer.seek(0)
        qr_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Store device information
        self.devices[username] = {
            'secret': secret,
            'registered_at': datetime.now().isoformat()
        }
        self._save_devices()
        
        return {
            'success': True,
            'message': f"Device registered successfully for {username}",
            'qr_code': qr_base64
        }

    def verify_code(self, username, code):
        if username not in self.devices:
            return {'success': False, 'message': 'User not registered'}
        
        secret = self.devices[username]['secret']
        totp = pyotp.TOTP(secret)
        
        if totp.verify(code):
            return {
                'success': True,
                'message': 'Authentication successful!'
            }
        return {
            'success': False,
            'message': 'Invalid code. Authentication failed.'
        }

# Initialize MFA demo
mfa = MFADemo()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'})
    
    result = mfa.register_device(username)
    return jsonify(result)

@app.route('/verify', methods=['POST'])
def verify():
    username = request.json.get('username')
    code = request.json.get('code')
    
    if not username or not code:
        return jsonify({'success': False, 'message': 'Username and code are required'})
    
    result = mfa.verify_code(username, code)
    
    if result['success']:
        try:
            with open('img/success.gif', 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                result['reward_image'] = img_data
        except FileNotFoundError:
            result['reward_image'] = None
            result['message'] += " (Reward image not found)"
    else:
        try:
            with open('img/impostor.gif', 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                result['reward_image'] = img_data
        except FileNotFoundError:
            result['reward_image'] = None
            result['message'] += " (Reward image not found)"

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
