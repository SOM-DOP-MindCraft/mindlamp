import json
import os
from flask import Flask, redirect, request
import requests

app = Flask(__name__)

# Load authorized users
with open('authorized_users.json', 'r') as f:
    AUTHORIZED_USERS = json.load(f)['allowed_users']

CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI')

@app.route('/login')
def login():
    return redirect(
        f'https://github.com/login/oauth/authorize?'
        f'client_id={CLIENT_ID}&'
        f'redirect_uri={REDIRECT_URI}&'
        'scope=user:email'
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Exchange code for access token
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        },
        headers={'Accept': 'application/json'}
    )
    
    access_token = token_response.json().get('access_token')
    
    # Get user info
    user_response = requests.get(
        'https://api.github.com/user', 
        headers={'Authorization': f'token {access_token}'}
    )
    
    username = user_response.json().get('login')
    
    # Check authorization
    if username in AUTHORIZED_USERS:
        return redirect('/index.html?token=' + access_token)
    else:
        return "Unauthorized", 403
