# Docker Historian

Python script to recover Docker file from an image.

Needs `docker-py` to run.

```
virtualenv -p python venv
. venv/bin/activate
pip install -r requirements.txt
```

## Running

```
./docker-historian.py [image name]
```

You can use partial image names.
