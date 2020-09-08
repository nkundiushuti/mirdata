import argparse
import glob
import hashlib
import json
import os
import string

DATASET_INDEX_PATH = '../mirdata/indexes/phenicx_anechoic_index.json'


def md5(file_path):
    """Get md5 hash of a file.

    Parameters
    ----------
    file_path: str
        File path.

    Returns
    -------
    md5_hash: str
        md5 hash of data in file_path
    """
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as fhandle:
        for chunk in iter(lambda: fhandle.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_dataset_index(data_path):

    pieces = ['beethoven','bruckner','mahler','mozart']
    totalinstruments = [20,39,30,10]
    ninstruments = [10,10,10,8]
    index = {}

    for ip,piece in enumerate(pieces):
        index[piece] = {}

        audio_files = sorted(
            glob.glob(os.path.join(data_path, 'audio', piece, '*.wav'))
        )
        instruments = [os.path.basename(audio_path).split('.')[0].rstrip(string.digits)
                        for audio_path in audio_files]
        set_instruments = list(set(instruments))
        assert len(instruments)==totalinstruments[ip],'audio files for some instruments are missing'
        assert len(set_instruments)==ninstruments[ip],'some instruments are missing from the dataset'

        for instrument in set_instruments:
            assert os.path.exists(os.path.join(data_path, 'annotations', piece,'{}.txt'.format(instrument))),'cannot find notes file {}'.formatos.path.join(data_path, 'annotations', piece,'{}.txt'.format(instrument))
            assert os.path.exists(os.path.join(data_path, 'annotations', piece,'{}_o.txt'.format(instrument))),'cannot find notes file {}'.formatos.path.join(data_path, 'annotations', piece,'{}_o.txt'.format(instrument))
            assert os.path.exists(os.path.join(data_path, 'annotations', piece,'{}.mid'.format(instrument))),'cannot find notes file {}'.formatos.path.join(data_path, 'annotations', piece,'{}.mid'.format(instrument))
            assert os.path.exists(os.path.join(data_path, 'annotations', piece,'{}_o.mid'.format(instrument))),'cannot find notes file {}'.formatos.path.join(data_path, 'annotations', piece,'{}_o.mid'.format(instrument))
            notes_checksum = md5(os.path.join(data_path, 'annotations', piece,'{}.txt'.format(instrument)))
            notes_original_checksum = md5(os.path.join(data_path, 'annotations', piece,'{}_o.txt'.format(instrument)))
            midi_checksum = md5(os.path.join(data_path, 'annotations', piece,'{}.mid'.format(instrument)))
            midi_original_checksum = md5(os.path.join(data_path, 'annotations', piece,'{}_o.mid'.format(instrument)))

            instrument_audio_files = sorted(
                glob.glob(os.path.join(data_path, 'audio', piece, instrument+'*.wav'))
                )
            assert len(instrument_audio_files)>0, 'no audio has been found for {}'.format(instrument)

            audio_dict={}
            for i,audio_file in enumerate(instrument_audio_files):
                audio_checksum = md5(
                    os.path.join(data_path, 'audio', piece, os.path.basename(audio_file))
                )
                audio_dict[i]=('audio/{}/{}'.format(piece,os.path.basename(audio_file)), audio_checksum)

            index[piece][instrument] = {
                'audio': audio_dict,
                'notes': ('annotations/{}/{}.txt'.format(piece,instrument), notes_checksum),
                'notes_original': ('annotations/{}/{}_o.txt'.format(piece,instrument), notes_original_checksum),
                'midi': ('annotations/{}/{}.mid'.format(piece,instrument), midi_checksum),
                'midi_original': ('annotations/{}/{}_o.mid'.format(piece,instrument), midi_original_checksum),
            }

        #import pdb;pdb.set_trace()

    with open(DATASET_INDEX_PATH, 'w') as fhandle:
        json.dump(index, fhandle, indent=2)


def main(args):
    make_dataset_index(args.data_path)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Make Phenicx-anechoic index file.')
    PARSER.add_argument(
        'data_path', type=str, help='Path to Phenicx-anechoic data folder.'
    )

    main(PARSER.parse_args())
