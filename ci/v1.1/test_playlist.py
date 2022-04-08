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


@pytest.fixture
def create_pl(plserv):
    # Create empty playlist
    name = "playlist_0"
    trc, p_id = plserv.create(name)
    assert trc == 200
    yield p_id
    # Cleanup called after the test completes
    plserv.delete(p_id)


def test_create_read(plserv):
    # Create playlist
    song = 'Respect'
    name = "playlist_1"
    trc, p_id = plserv.create(name, song)
    assert trc == 200

    # Read playlist
    trc, playlistName, songs = plserv.read(p_id)
    assert (trc == 200 and playlistName == name and songs == [song])

    # Delete objects
    plserv.delete(p_id)


def test_read_update(plserv, create_pl):
    # Read playlist
    name = "playlist_0"
    trc, playlistName, songs = plserv.read(create_pl)
    assert (trc == 200 and playlistName == name and songs == [])
    # Update playlist
    # song = 'My heart will go on'
    # plserv.update(create_pl, song)
