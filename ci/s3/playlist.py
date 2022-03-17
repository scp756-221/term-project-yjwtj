"""
Python  API for the playlist service.
"""

<<<<<<< HEAD
# Installed packages
import requests

class Playlist():
    """Python API for the music service.
=======
# Standard library modules

# Installed packages
import requests


class Playlist():
    """Python API for the Playlist service.
>>>>>>> jeff

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
<<<<<<< HEAD
        'http://cmpt756s2:{port_number}/'. Note the trailing slash.
=======
        'http://cmpt756s2:30001/'. Note the trailing slash.
>>>>>>> jeff
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

<<<<<<< HEAD
    def read(self, p_id):
        """Read a playlist by its p_id.

        Args:
            p_id (string):
                The UUID of this playlist in database.

        Returns:
            status_code
            PlayListName (string)
            SongList (list<string>)
        """
        response = requests.get(
            self._url + p_id,
            headers={"Authorization": self._auth}
        )
        if response.status_code != 200:
            # Failed
            return response.status_code, None, None
        
        item = response.json()["items"][0]
        return response.status_code, item["PlayListName"], \
               item["SongList"]
               
    def update(self, p_id, song_list):
        """Update a playlist by given song list.

        Args:
            p_id (string)
            song_list (list<string>)

        Returns:
            status_code: denotes whether operation has succeeded
        """
        response = requests.put(
            self._url + p_id,
            headers={"Authorization": self._auth},
            json={"SongList": song_list}
        )
        return response.status_code
=======
    def create(self, list_name, song=None):
        """Create a playlist.

        Parameters
        ----------
        list_id: string
            The id of the playlist.
        list_name: string
            The name of the playlist.
        song: string
            The song to be added to the playlist.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by PlayList.
            The string is the UUID of this playlist in the play list database.
        """
        if read(list_name) is not None:
            return Response(json.dumps({"error": "There is alread this list"}),
                        status=401,
                        mimetype='application/json')
        
        payload = {'PlayListName': list_name,
                  'PlayList': []}
        if song is not None:
            payload['PlayList'].append(song)
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

     def delete(self, p_id):
        """Delete the playlist

        Parameters
        ----------
        m_id: string
            The UUID of this playlist in the play list database.

        Returns
        -------
        Does not return anything. The playlist delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )
>>>>>>> jeff
