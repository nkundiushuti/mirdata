from __future__ import absolute_import

import os

import numpy as np
import pytest

from mirdata import dali, utils
from tests.test_utils import  DEFAULT_DATA_HOME


def test_track():
    # test data home None
    track_default = dali.Track('0111')  # TODO: track name
    assert track_default._data_home == os.path.join(DEFAULT_DATA_HOME, 'Dali')

    data_home = 'tests/resources/mir_datasets/Dali'

    with pytest.raises(ValueError):
        dali.Track('asdf', data_home=data_home)

    track = dali.Track('0111', data_home=data_home) # TODO: track name
    assert track.track_id == '0111' # TODO: track name
    assert track._data_home == data_home
    assert track._track_paths == { # TODO: track name
        'audio': [
            'audio/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.wav',
            '1b57c2f78ae0f19eed1ae7fbf747e12d',
        ],
        'beat': [
            'annotations/beat/The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.txt',
            'f698ad2d802bf62fe10f59ea8b4af9f6',
        ],
        'chords': [
            'annotations/chordlab/The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab',
            '24f12726a510c0321aa06cac95f27915',
        ],
        'keys': [
            'annotations/keylab/The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab',
            'ca194503b783ed20521a1429411f3094',
        ],
        'sections': [
            'annotations/seglab/The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab',
            '509125d527dae09cdee832fc0a6e0580',
        ],
    }
    assert (
        track.audio_path
        == 'tests/resources/mir_datasets/Dali/' # TODO: track name
        + 'audio/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.wav'
    )
    assert track.title == '11_-_Do_You_Want_To_Know_A_Secret'
    assert type(track.notes) == utils.NoteData
    assert type(track.words) ==
    assert type(track.paragraphs) ==
    assert type(track.annotation_object) ==

    audio, sr = track.audio
    assert sr == 44100  # TODO: true?
    assert audio.shape == (44100 * 2,)

    repr_string = ( # TODO: change
        "Beatles Track(track_id=0111, "
        + "audio_path=tests/resources/mir_datasets/Beatles/audio/"
        + "01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.wav, "
        + "title=11_-_Do_You_Want_To_Know_A_Secret, "
        + "beats=BeatData('beat_times, 'beat_positions'), "
        + "chords=ChordData('start_times', 'end_times', 'chords'), "
        + "key=KeyData('start_times', 'end_times', 'keys'), "
        + "sections=SectionData('start_times', 'end_times', 'sections'))"
    )
    assert track.__repr__() == repr_string

    track = dali.Track('10212')  # TODO any missing annotations we should check?
    assert track.beats == None
    assert track.key == None


def test_track_ids():
    track_ids = dali.track_ids()
    assert type(track_ids) is list
    assert len(track_ids) == 180  # TODO change


def test_load():
    data_home = 'tests/resources/mir_datasets/Dali'
    dali_data = dali.load(data_home=data_home)
    assert type(dali_data) is dict
    assert len(dali_data.keys()) == 180  # TODO change

    dali_data_default = dali.load()
    assert type(dali_data_default) is dict
    assert len(dali_data_default.keys()) == 180  # TODO change


def test_load_beats():  # TODO have to test all data types
    dali_path = (
        'tests/resources/mir_datasets/Dali/annotations/beat/'  # TODO change
        + 'The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.txt'
    )
    beat_data = beatles._load_beats(beats_path)

    assert type(beat_data) == utils.BeatData
    assert type(beat_data.beat_times) == np.ndarray
    assert type(beat_data.beat_positions) == np.ndarray

    assert np.array_equal(
        beat_data.beat_times,
        np.array([13.249, 13.959, 14.416, 14.965, 15.453, 15.929, 16.428]),
    )
    assert np.array_equal(beat_data.beat_positions, np.array([2, 3, 4, 1, 2, 3, 4]))

    # load a file which doesn't exist
    beat_none = beatles._load_beats('fake/file/path')
    assert beat_none is None


def test_load_chords():
    chords_path = (
        'tests/resources/mir_datasets/Beatles/annotations/chordlab/'
        + 'The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab'
    )
    chord_data = beatles._load_chords(chords_path)

    assert type(chord_data) == utils.ChordData
    assert type(chord_data.start_times) == np.ndarray
    assert type(chord_data.end_times) == np.ndarray
    assert type(chord_data.chords) == np.ndarray

    assert np.array_equal(
        chord_data.start_times, np.array([0.000000, 4.586464, 6.989730])
    )
    assert np.array_equal(
        chord_data.end_times, np.array([0.497838, 6.989730, 9.985104])
    )
    assert np.array_equal(chord_data.chords, np.array(['N', 'E:min', 'G']))

    # load a file which doesn't exist
    chord_none = beatles._load_chords('fake/file/path')
    assert chord_none is None


def test_load_key():
    key_path = (
        'tests/resources/mir_datasets/Beatles/annotations/keylab/'
        + 'The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab'
    )
    key_data = beatles._load_key(key_path)

    assert type(key_data) == utils.KeyData
    assert type(key_data.start_times) == np.ndarray

    assert np.array_equal(key_data.start_times, np.array([0.000]))
    assert np.array_equal(key_data.end_times, np.array([119.333]))
    assert np.array_equal(key_data.keys, np.array(['E']))

    # load a file which doesn't exist
    key_none = beatles._load_key('fake/file/path')
    assert key_none is None


def test_load_sections():
    sections_path = (
        'tests/resources/mir_datasets/Beatles/annotations/seglab/'
        + 'The Beatles/01_-_Please_Please_Me/11_-_Do_You_Want_To_Know_A_Secret.lab'
    )
    section_data = beatles._load_sections(sections_path)

    assert type(section_data) == utils.SectionData
    assert type(section_data.start_times) == np.ndarray
    assert type(section_data.end_times) == np.ndarray
    assert type(section_data.sections) == np.ndarray

    assert np.array_equal(section_data.start_times, np.array([0.000000, 0.465]))
    assert np.array_equal(section_data.end_times, np.array([0.465, 14.931]))
    assert np.array_equal(section_data.sections, np.array(['silence', 'intro']))

    # load a file which doesn't exist
    section_none = beatles._load_sections('fake/file/path')
    assert section_none is None



def test_validate():
    dali.validate()
    dali.validate(silence=True)


def test_cite():
    dali.cite()