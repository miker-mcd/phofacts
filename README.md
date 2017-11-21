# phofacts
A web application for helpful facts about nearby pho restaurants.

## How to Install phofacts
- First, ensure that you have the latest version of Python installed on your machine
- Clone the repository to your local machine and navigate into the phofacts directory
- Install Flask using the following [guide](http://flask.pocoo.org/docs/0.12/installation/#installation)
- Obtain a [Google Maps API key](https://developers.google.com/maps/documentation/embed/get-api-key) and set up the environment variable for the key by installing [python-dotenv](https://simpleit.rocks/managing-environment-configuration-variables-in-flask-with-dotenv/)
- Next, export the FLASK_APP environment and enable debug mode by entering the following commands into your terminal:
```
$ export FLASK_APP=hello.py
$ export FLASK_DEBUG=1
$ flask run
```
If you are on Windows you need to use `set` instead of `export`.
The last command will launch the local server.
- Check to see if the server is running by visiting http://localhost:5000 in your browser and you should see "Hello, World!"
- If the server is not running or if there are any issues, the following [guide](http://flask.pocoo.org/docs/0.12/quickstart/#quickstart) may be helpful

## The Team
- [Michael McDonald](https://github.com/miker-mcd)
- [Tony Brackins](https://github.com/mrbrackins)
- [Wing Ng](https://github.com/citrusapple)
- [Marco Antonio Gutierrez](https://github.com/MarcoGutierrez)
