from flask import Flask, redirect, url_for, session, request, render_template_string
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = str(os.getenv("secret_key"))  # Use a secure secret key

# Allow HTTP for local dev
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

# Home page with buttons
@app.route('/')
def index():
    return render_template_string('''
        <h2>Welcome to the YouTube App</h2>
        <a href="{{ url_for('login') }}"><button>Login</button></a>
        <a href="#"><button>Reply</button></a>
    ''')

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Save the token in environment variable (only for session/lab use; not secure for prod)
    os.environ['YOUTUBE_ACCESS_TOKEN'] = credentials.token
    with open(".env", "a") as f:
         f.write(f"token={credentials.token}\n")

    # Optionally store in session (if needed for other routes)
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return render_template_string('''
        <h3>Login successful!</h3>
        <p>Access token saved to environment variable.</p>
        <a href="{{ url_for('index') }}"><button>Go back to Home</button></a>
    ''')

@app.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))

@app.route('/show_token')
def show_token():
    token = os.environ.get('YOUTUBE_ACCESS_TOKEN', 'No token found')
    return "token:" + str(os.getenv("token"))


if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
