Based on the supporting code for the article [video streaming with Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask) and its follow-up [Flask Video Streaming Revisited](http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited).

use:

create a virtualenv and load it, install dependencies...

```
virtualenv headmouse
source headmouse/bin/activate
pip install -r requirements.txt
CAMERA=opencv gunicorn --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app
open: http://0.0.0.0:5000
```


on heroku: you need to add apt buildpack support with: heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt then git push heroku master 
