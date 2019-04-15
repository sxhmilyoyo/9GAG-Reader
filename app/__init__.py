from bs4 import BeautifulSoup
import feedparser
from flask import Flask, render_template
from flask_caching import Cache
import requests
import logging
from logging import FileHandler, INFO
from logging.config import dictConfig
import os
import json
from PIL import Image
import requests
from io import BytesIO

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'app.log',
        'formatter': 'default',
        'level': 'INFO'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route('/', methods=['GET'])
def home_page():
    feed_names = ['Awesome', 'DarkHumor', 'Funny', 'Hot']
    return render_template('feeds.html', is_root=True, feed_names=feed_names)


@app.route('/feeds/<feed_name>', methods=['GET'])
@cache.cached(timeout=120)
def show_feed(feed_name):
    app.logger.info("request")
    url = 'https://9gag-rss.com/api/rss/get?code=9GAG{}&format=1'.format(
        feed_name)
    feed_contents = feedparser.parse(url)
    entries = feed_contents.entries
    widths = list()
    for entry in entries:
        html_doc = entry['content'][0]['value']
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.video:
            width = soup.video['width']
        elif soup.img:
            src = soup.img['src']
            response = requests.get(src)
            img = Image.open(BytesIO(response.content))
            width = '{}px'.format(str(img.size[0]))
        else:
            width = ""
        widths.append(width)
    # with open("./entries.json", "w") as fp:
    #     json.dump(feed_contents.entries, fp, indent=4)
    return render_template('content.html', is_root=False, feed_name=feed_name, entries=entries, widths=widths)


# api_port = int(os.environ.get("API_PORT", 700))
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=api_port, debug=True)
