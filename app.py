from flask import Flask, redirect, request, session, url_for
import os
from requests_oauthlib import OAuth2Session
app = Flask(__name__)

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
APP_SECRET = os.getenv('APP_SECRET', 'development')

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
base_url = 'https://github.com/'
github_api_url = 'https://api.github.com/'

owner = os.environ['owner']
repo = os.environ['repo']

app.secret_key = APP_SECRET


""" 
I used the following documentation and github projects as guides

-Working example of what was asked for, good starting point
https://github.com/andheroe/self-replicating-repository-1/blob/master/ 

-Documentation on how to register your app with github, and interact with its authorization lib
https://developer.github.com/apps/building-oauth-apps/ 
https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/

-example of using 0Auth2Session
https://docs.authlib.org/en/latest/client/oauth2.html
https://requests-oauthlib.readthedocs.io/en/latest/

"""


@app.route("/")
def authorize_user():

    github = OAuth2Session(client_id, scope="public_repo")
    uri, state = github.authorization_url(authorization_base_url)
    return redirect(uri)


@app.route("/callback")
def callback():

    github = OAuth2Session(client_id)
    token = github.fetch_token(client_id=client_id, client_secret=client_secret, token_url=token_url,
                               authorization_response=request.url)
    # session is a global variable of Flask
    session['auth_token'] = token
    return redirect(url_for('replicate'))


@app.route("/replicate")
def replicate():
    if not session['auth_token']:
        return "you were not authorized to replicate this project"

    github = OAuth2Session(client_id, token=session['auth_token'])

    print(github_api_url + 'repos/' + owner + '/' + repo + '/forks')

    response = github.post(github_api_url + 'repos/' + owner + '/' + repo + '/forks')

    print('Status Code:' + str(response.status_code))
    if response.status_code == 404:
        return "the url provided does not exist"

    return "done"


if __name__ == "__main__":
    # Uncomment the below line to run via HTTP - don't use in production
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run()


