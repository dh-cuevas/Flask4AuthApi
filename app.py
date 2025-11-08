import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth

# Cargar variables de entorno
load_dotenv()

# Configurar Flask
app = Flask(__name__)
# app.secret_key = os.urandom(24)
app.secret_key = os.getenv('SECRET_KEY')

# Configurar Auth0
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    server_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Ruta principal
@app.route('/')
def home():
    user_info = session.get('user')
    return render_template('login.html', user=user_info)

# Ruta de login
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))

# Ruta de callback
@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?returnTo={os.getenv('AUTH0_LOGOUT_URL')}&client_id={os.getenv('AUTH0_CLIENT_ID')}"
    )

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
