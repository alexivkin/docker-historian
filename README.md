# Docker Historian

Python script to recover Docker file from an image.

## Running natively

Install `docker-py` to run.

``` bash
virtualenv -p python venv
. venv/bin/activate
pip install -r requirements.txt
```

Then `./docker-historian.py [image name]`

You can use partial image names.


## Running from container

You need to share your dockerd's socket with the historian. Run `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock alexivkin/docker-historian [image name]`
