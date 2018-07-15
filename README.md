configuración inicial basada en: https://github.com/dxue2012/python-webcam-flask 

### Setup

#### Optional

- install heroku cli https://devcenter.heroku.com/articles/heroku-cli
- Use a python virtualenv: (install virtualenv + virtualenv headmouse + source headmouse/bin/activate) 

#### Required
- `git clone https://github.com/dxue2012/python-webcam-flask.git`
- `pip install -r requirements.txt`

### Run locally

IF YOU HAVE HEROKU:
- `heroku local`
IF NOT:
- `gunicorn -k eventlet -w 1 app:app --log-file=-`

- in your browser, navigate to localhost:5000

### Deploy to heroku

- `git push heroku master`
- heroku open

### Common Issues

If you run into a 'protocol not found' error, see if [this stackoverflow answer helps](https://stackoverflow.com/questions/40184788/protocol-not-found-socket-getprotobyname).
