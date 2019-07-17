<h1>Self Replicating App:</h1> 
The following is a web app that self replicates itself in github. \
Below are the steps to run it both locally and on Heroku.

<h2>Overview of App Flow: </h2>
1. User clicks on url and is redirected to github
2. User signs in to authorize forking of project
3. The application will fork its own repo to the Users profile.

<h2>How to Install:</h2>
<h3>Prep work:<h3>
1. Register your app on <a href="https://github.com/settings/applications/new">github</a>
2. Name your application something people will trust or recognize.
3. Provide the url where your app is sitting. If running locally provide the local url, e.g. http://127.0.0.1:5000/ 
4. The callback url must match the url that will receive the token. By default the url for this project is <i>hostname</i>/callback.
5. Keep track of your client id and client secret, you will need both.

<h3>Run locally:</h3> 
1. clone the project: https://github.com/CJG3/SelReplicatingGit.git
2. Set up the following environment variables described below
    1. client_id = client id given upon registration \
    2. client_secret = client secret given upon registration \
    3. owner = your github username
    4. the repo you cloned in step 1.
3. If you don't have it, <a href="https://www.python.org/downloads/">Download</a> and install python appropriate to your environment.
4. Follow the steps provided in this <a href="https://flask.palletsprojects.com/en/1.1.x/installation/">documentation</a> to install Flask. You can skip the venv as this project provides it for you.
5. Once the project is set up, you should be able to go to the project directory and execute the 'run flask' command. Once completed, flask provides a url which you can click on and it will take you to the web app.


<h3>Run on Heroku:</h3>
1. If you don't have an account, click <a href = "https://signup.heroku.com/">here</a>
2. If you have one, sign in <a href = "https://id.heroku.com/login">here</a>
3. Select new app, follow the deployment instructions provided.
4. On the activity tab be sure to add the environment variables mentioned above in how to run locally.
5. From there your app should be complete and ready to try.