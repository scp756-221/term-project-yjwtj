"""
Test the *_original_artist routines.
These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import playlist


@pytest.fixture
def plserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


def create_pl(plserv, list_name):
    # Helper to create a playlist when testing
    trc, p_id = plserv.create(list_name)
    assert trc == 200
    return p_id


def test_delete(plserv):
    name = "some_playlist"
    p_id = create_pl(plserv, name)
    plserv.delete(p_id)

    # Check deletion successful
    trc, playlistName, songs = plserv.read(p_id)
    assert trc == 404 and \
        playlistName is None and \
        songs is None
    # Clean up no longer requried as deletion was tested


def test_create_read(plserv):
    songs = ["Snow in june", "Voice over tested", "Demon"]
    name = "some_other_playlist"
    trc, p_id = plserv.create(name, songs)
    assert trc == 200

    # Read playlist
    trc, r_name, r_songs = plserv.read(p_id)
    assert trc == 200 and r_name == name and songs == r_songs

    # Delete objects
    plserv.delete(p_id)


def test_read_and_update(plserv):
    name = "playlist_empty"
    p_id = create_pl(plserv, name)

    # Read and check empty playlist
    trc, playlistName, songs = plserv.read(p_id)
    assert trc == 200 and \
           playlistName == name and \
           songs == []

    # Update playlist
    new_song_list = ['My heart will go on', "Respect"]
    trc = plserv.update(p_id, new_song_list)
    assert trc == 200

    # Check update successful
    trc, playlistName, songs = plserv.read(p_id)
    assert trc == 200 and \
        playlistName == name and \
        songs == new_song_list

    # Cleanup called after the test completes
    plserv.delete(p_id)
