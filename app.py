from flask import Flask, redirect, request, session, url_for
import os
from requests_oauthlib import OAuth2Session
app = Flask(__name__)

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
owner = os.environ['owner']
repo = os.environ['repo']
APP_SECRET = os.getenv('APP_SECRET', 'development')

authorization_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
github_api_url = 'https://api.github.com/'



app.secret_key = APP_SECRET


""" 
I used the following documentation and github projects as guides

-Working example of what was asked for, good starting point
https://github.com/andheroe/self-replicating-repository-1

-Documentation on how to register your app with github, and interact with its authorization lib
https://developer.github.com/apps/building-oauth-apps/ 
https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/

-example of using 0Auth2Session
https://docs.authlib.org/en/latest/client/oauth2.html
https://requests-oauthlib.readthedocs.io/en/latest/

"""


@app.route("/")
def authorize_user():

    """First authorize the user. We redirect them to the
    authorization url provided in documentation on github"""
    github = OAuth2Session(client_id, scope="public_repo")
    uri, state = github.authorization_url(authorization_url)
    return redirect(uri)


"""The call back is the url we provide during registration step.
https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/"""
@app.route("/callback")
def callback():

    """creates an instance of the 0Auth with our client Id and gets the token."""
    github = OAuth2Session(client_id)
    token = github.fetch_token(client_id=client_id, client_secret=client_secret, token_url=token_url,
                               authorization_response=request.url)
    # session is a global variable of Flask
    session['auth_token'] = token
    return redirect(url_for('replicate'))


@app.route("/replicate")
def replicate():

    # Check to see if token was given.
    if not session['auth_token']:
        return "you were not authorized to replicate this project"

    """Creates a new instance of OAuth and authorizes with global token"""
    github = OAuth2Session(client_id, token=session['auth_token'])

    """Makes the post to create a fork as documented in github api docs 
    https://developer.github.com/v3/repos/forks/#create-a-fork"""
    response = github.post(github_api_url + 'repos/' + owner + '/' + repo + '/forks')

    # Checks to see if url exists
    if response.status_code == 404:
        return "the url provided does not exist"

    if response.status_code == 202:
        return "You have sucessfully forked your project " + repo

    return "something went wrong, please contact the author of this code."


if __name__ == "__main__":
    """ Uncomment the below line to run via HTTP, aka locally
    Do not use in production"""
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run()


