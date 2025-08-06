from flask import Flask, render_template, request, jsonify, send_file
import pyotp
import qrcode
import json
from pathlib import Path
from datetime import datetime
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

import time

class MFADemo:
    def __init__(self, storage_file="/app/data/registered_devices.json"):
        self.storage_file = Path(storage_file)
        self.lock_file = self.storage_file.with_suffix('.lock')
        self.devices = self._load_devices()

    def _acquire_lock(self, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Atomically create the lock file
                self.lock_file.touch(exist_ok=False)
                logging.info("File lock acquired.")
                return True
            except FileExistsError:
                time.sleep(0.1)
        logging.error("Could not acquire file lock.")
        return False

    def _release_lock(self):
        if self.lock_file.exists():
            self.lock_file.unlink()
            logging.info("File lock released.")

    def _load_devices(self):
        if self._acquire_lock():
            try:
                if self.storage_file.exists():
                    logging.info(f"Loading devices from {self.storage_file}")
                    with open(self.storage_file, 'r') as f:
                        try:
                            return json.load(f)
                        except json.JSONDecodeError:
                            logging.error(f"Could not decode JSON from {self.storage_file}. Starting with an empty device list.")
                            return {}
                logging.info("No storage file found. Starting with an empty device list.")
                return {}
            finally:
                self._release_lock()
        return {}


    def _save_devices(self):
        if self._acquire_lock():
            try:
                logging.info(f"Saving devices to {self.storage_file}")
                with open(self.storage_file, 'w') as f:
                    json.dump(self.devices, f, indent=4)
            finally:
                self._release_lock()

    def register_device(self, username):
        logging.info(f"Registering device for user: {username}")
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

        logging.info(f"Device registered successfully for user: {username}")
        return {
            'success': True,
            'message': f"Device registered successfully for {username}",
            'qr_code': qr_base64
        }

    def verify_code(self, username, code):
        logging.info(f"Verifying code for user: {username}")
        if username not in self.devices:
            logging.warning(f"Verification failed: User '{username}' not found.")
            return {'success': False, 'message': 'User not registered'}

        secret = self.devices[username]['secret']
        totp = pyotp.TOTP(secret)

        if totp.verify(code):
            logging.info(f"Verification successful for user: {username}")
            return {
                'success': True,
                'message': 'Authentication successful!'
            }
        logging.warning(f"Verification failed: Invalid code for user: {username}")
        return {
            'success': False,
            'message': 'Invalid code. Authentication failed.'
        }

def _get_reward_image(success):
    image_name = 'success.gif' if success else 'impostor.gif'
    try:
        with open(f'img/{image_name}', 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        logging.error(f"Could not find image: {image_name}")
        return None

# Initialize MFA demo
mfa = MFADemo()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    if not username or not username.strip():
        logging.error("Registration failed: Username is required and cannot be empty.")
        return jsonify({'success': False, 'message': 'Username is required and cannot be empty'})

    result = mfa.register_device(username.strip())
    return jsonify(result)

@app.route('/verify', methods=['POST'])
def verify():
    username = request.json.get('username')
    code = request.json.get('code')

    if not username or not code:
        logging.error("Verification failed: Username and code are required.")
        return jsonify({'success': False, 'message': 'Username and code are required'})

    result = mfa.verify_code(username, code)

    result['reward_image'] = _get_reward_image(result['success'])
    if not result['reward_image']:
        result['message'] += " (Reward image not found)"

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
