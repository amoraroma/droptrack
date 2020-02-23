from flask import current_app
from urllib.parse import urlparse
from subprocess import Popen


def file_allowed(filename):
    allowed_extensions = current_app.config.UPLOAD_ALLOWED_EXTENSIONS
    return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions


def validate_url(url):
    return url.startswith('http://') \
        or url.startswith('https://')


def validate_soundfile(soundfile):
    if soundfile is None or soundfile.filename == '':
        current_app.logger.info('No file')
        return False
    else:
        return file_allowed(soundfile.filename)


def push_to_queue(url):
    current_app.queue.send(url)


def download(url):
    scheme, netloc, path, *_ = urlparse(url)
    cmd = f'soundscrape {scheme}{netloc}/{path}'