from .fart import FART
from .matlab_recording import MatlabRecording


class Frames:

    def __init__(self, recording_software, filename=None,gridfs=None):
        print('Hello')

    def __new__(cls,filename=None, gridfs=None,recording_software='fart', **kwargs):
        if recording_software is RecordingSoftwares.fart:
            return FART(filename=filename, gridfs=gridfs, **kwargs)
        elif recording_software is RecordingSoftwares.matlab:
            return MatlabRecording(filename=filename, gridfs=gridfs)
        else:
            raise NameError('Recording software: ' + recording_software + ' is not supported')

    @property
    def list_of_recording_softwares(self):
        return [x for x in dir(RecordingSoftwares) if not x.startswith('__')]


class RecordingSoftwares:
    fart = 'fart'
    matlab = 'matlab'
