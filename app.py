import secrets
import string
import os
import re
from flask import Flask, request, jsonify, render_template
from database import init_db, check_duplicate_and_store

app = Flask(__name__, static_folder="static", template_folder="static")

# Initialize SQLite database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({"error": "No password provided"}), 400
        
    # Process password to check for database duplication (Archive Conflict)
    # The password is ONLY processed in memory. Zero plaintext policy.
    is_duplicate = check_duplicate_and_store(password)
    
    score = 0
    diagnostics = []
    
    length = len(password)
    if length < 8:
        diagnostics.append({"status": "error", "message": "✖ CRITICAL: Length strictly below 8 bits"})
    elif length < 12:
        diagnostics.append({"status": "warning", "message": "⚠ WARNING: Low entropy length (<12)"})
        score += 1
    elif length < 16:
        diagnostics.append({"status": "success", "message": "✓ ENTROPY CHECK PASSED: Adequate length (12+)"})
        score += 2
    else:
        diagnostics.append({"status": "success", "message": "✓ CRYPTOGRAPHIC LENGTH PASSED (16+ bits)"})
        score += 3
        
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    variety_score = sum([has_lower, has_upper, has_digit, has_special])
    if variety_score == 4:
        diagnostics.append({"status": "success", "message": "✓ FULL DISTRIBUTION: Upper, Lower, Digits, Symbols"})
        score += 1
    elif variety_score >= 3:
        diagnostics.append({"status": "warning", "message": "⚠ PARTIAL DISTRIBUTION: Missing character types"})
    else:
        diagnostics.append({"status": "error", "message": "✖ CRITICAL: Poor character distribution"})
        
    # Check for patterns
    lower_pw = password.lower()
    patterns = ['12345', '23456', 'abcde', 'qwerty', 'asdfg', 'zxcvb', 'password', 'admin', '123123']
    
    has_pattern = False
    for pat in patterns:
        if pat in lower_pw:
            has_pattern = True
            break
            
    if has_pattern:
        diagnostics.append({"status": "error", "message": "⚠ SEQUENTIAL/DICTIONARY PATTERN DETECTED"})
        score = min(score, 1) # Cap score
    else:
        diagnostics.append({"status": "success", "message": "✓ ALGORITHMIC PATTERN FILTERING PASSED"})
        
    # Archive conflict check
    if is_duplicate:
        diagnostics.insert(0, {"status": "error", "message": "⚠️ ARCHIVE CONFLICT: Matches historical profile."})
        score = 0
        
    if score > 4:
        score = 4
        
    return jsonify({
        "duplicate": is_duplicate,
        "score": score,
        "diagnostics": diagnostics
    })

@app.route('/api/generate', methods=['GET'])
def generate():
    """
    Cryptographically Secure Generation Engine utilizing CSPRNG.
    Enforces at least 2 uppercase, 2 lowercase, 2 numbers, and 2 special symbols.
    """
    length = 16
    upper = [secrets.choice(string.ascii_uppercase) for _ in range(2)]
    lower = [secrets.choice(string.ascii_lowercase) for _ in range(2)]
    digits = [secrets.choice(string.digits) for _ in range(2)]
    special = [secrets.choice("!@#$%^&*()-_=+") for _ in range(2)]
    
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    remaining_length = length - 8
    remaining = [secrets.choice(all_chars) for _ in range(remaining_length)]
    
    password_list = upper + lower + digits + special + remaining
    
    # Securely shuffle to eradicate structural predictability
    secrets.SystemRandom().shuffle(password_list)
    secure_password = ''.join(password_list)
    
    return jsonify({
        "password": secure_password
    })

if __name__ == '__main__':
    # Ensure static directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    app.run(debug=True, port=5000)
