"""
Python  API for the playlist service.
"""

# Installed packages
import requests


class Playlist():
    """Python API for the Playlist service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:{port_number}/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

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

        r = response.json()

        if r["Count"] == 0:
            return 404, None, None
        else:
            item = r["Items"][0]
            return response.status_code, item["PlayListName"], item["SongList"]

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

    def create(self, list_name, songs=[]):
        """Create a playlist.

        Parameters
        ----------
        list_id: string
            The id of the playlist.
        list_name: string
            The name of the playlist.
        song: list<string>
            The songs to be added to the playlist when creating.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by PlayList.
            The string is the UUID of this playlist in the play list database.
        """
        payload = {"PlayListName": list_name,
                   "SongList": songs}

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
