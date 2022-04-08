"""
SFU CMPT 756
The playlist service.
"""

# Standard library modules
import logging
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics
import requests
import simplejson as json

# The application
app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    # list all playlists here
    url = db["name"] + '/' + db["endpoint"][0]  # read
    response = request.get(url,
                           params={"objtype": "playlist",
                                   "objkey": ''},
                           headers={'Authorization':
                                    headers['Authorization']})
    return response.json()


@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """
    Read the corresponding playlist
    """
    headers = request.headers
    if "Authorization" not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    url = db["name"] + '/' + db["endpoint"][0]  # read
    response = requests.get(url,
                            params={"objtype": "playlist",
                                    "objkey": playlist_id},
                            headers={'Authorization':
                                     headers['Authorization']})
    return response.json()


@bp.route("/<playlist_id>", methods=["PUT"])
def update_playlist(playlist_id):
    """
    Update the playlist's songs with a given song list
    """
    headers = request.headers
    if "Authorization" not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')

    try:
        content = request.get_json()
        song_list = content['SongList']  # this should be a list of songIds
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    # Check if song exists in Songs TODO
    url = db["name"] + '/' + db["endpoint"][3]
    response = requests.put(url,
                            params={"objtype": "playlist",
                                    "objkey": playlist_id},
                            headers={'Authorization':
                                     headers['Authorization']},
                            json={"SongList": song_list}
                            )
    return (response.json())


@bp.route('/', methods=['POST'])
def create_list():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        playlist_name = content['PlayListName']
        song_list = content['SongList']
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(url,
                             json={"objtype": "playlist",
                                   "PlayListName": playlist_name,
                                   "SongList": song_list},
                             headers={'Authorization':
                                      headers['Authorization']})
    return (response.json())


@bp.route('/<p_id>', methods=['DELETE'])
def delete_list(p_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params={"objtype": "playlist", "objkey": p_id},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
