# abatement_of_fake_news

In this project we created a web application which takes data uploaded on sharing pages of social media and checks it for pre registered hot words. if a match is found a query request is sent to concerned authority to verify the data. the data is added to a blockchain along with the verification sent by the authority. adding it to the blockchain allows us to create a decentralized consensus about the validity of the proof. The data is then added on to the site.

## Instructions to run

Clone the project,

```sh
$ git clone https://github.com/satwikkansal/python_blockchain_app.git
```

Install the dependencies,

```sh
$ cd python_blockchain_app
$ pip install -r requirements.txt
```

Start a blockchain node server,

```sh
# Windows users can follow this: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
$ export FLASK_APP=node_server.py
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.


Run the application on a different terminal session,

```sh
$ python run_app.py
```

