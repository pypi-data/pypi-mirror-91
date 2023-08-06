"""
read.py
    Functions for reading single entries from seq files.
"""
from os import remove
from pypulseq.Sequence.sequence import Sequence
from bmctool.sim.utils.seq.conversion import convert_seq_13_to_12


def get_minor_version(seq_file: str) -> int:
    """
    :param seq_file: path to the sequence file to read into the Sequence object
    :return version: version from the sequence file
    """
    with open(seq_file) as file:
        for line in file:
            if line.startswith('minor'):
                return int(line[len('minor '):])


def read_any_version(seq_file: str,
                     dev_version: bool = True,
                     seq: Sequence = None) \
        -> Sequence:
    """
    reading a sequence file of any version
    :param seq_file: path to the sequence file to read into the Sequence object
    :param dev_version: convert to dev-branch version 1.2 ?
    :param seq: the sequence to read the seq file into. If not provided, a new Sequence object is instantiated
    :return seq: Sequence object
    """
    version = get_minor_version(seq_file)
    if not seq:
        seq = Sequence()
    if version == 2:
        seq.read(seq_file)
    elif version == 3:
        tmp_file = convert_seq_13_to_12(seq_file, dev_version=dev_version, temp=True)
        seq.read(tmp_file)
        remove(tmp_file)
    else:
        raise ValueError('Version', version, 'can not be converted.')
    return seq
