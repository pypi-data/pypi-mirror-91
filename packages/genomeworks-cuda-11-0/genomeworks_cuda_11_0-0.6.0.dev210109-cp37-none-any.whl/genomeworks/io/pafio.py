#
# Copyright 2019-2020 NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Functions for PAF I/O."""
from collections import namedtuple


__all__ = ["read_paf", "write_paf", "Overlap"]


FIELDS = [
    "query_sequence_name",
    "query_sequence_length",
    "query_start",
    "query_end",
    "relative_strand",
    "target_sequence_name",
    "target_sequence_length",
    "target_start",
    "target_end",
    "num_residue_matches",
    "alignment_block_length",
    "mapping_quality",
    "tags",
]

Overlap = namedtuple("Overlap", FIELDS)

SAM_TYPES = {"i": int, "A": str, "f": float, "Z": str}
REV_TYPES = {
    "tp": "A",
    "cm": "i",
    "s1": "i",
    "s2": "i",
    "NM": "i",
    "MD": "Z",
    "AS": "i",
    "ms": "i",
    "nn": "i",
    "ts": "A",
    "cg": "Z",
    "cs": "Z",
    "dv": "f",
    "de": "f",
    "rl": "i",
}


def _parse_tags(tags):
    """Convert a list of SAM style tags, from a PAF file, to a dict.

    https://samtools.github.io/hts-specs/SAMv1.pdf section 1.5

    Args:
        tags (list): A list of SAM style tags.

    Returns (dict):
        Dict of typed SAM style tags

    """
    return {
        tag: _conv_type(val, SAM_TYPES.get(type_))
        for tag, type_, val in (x.split(":") for x in tags)
    }


def _conv_type(s, func):
    """Generic converter, to change strings to other types.

    Args:
        s (str): String that represents another type.
        func (function): Function to convert s, should take a singe parameter
            eg: int(), float()

    Returns:
        The type of func, otherwise str

    """
    if func is not None:
        try:
            return func(s)
        except ValueError:
            return s
    return s


def _tags_to_str(tags):
    """Convert dict of SAM style tags to a string.

    Args:
        tags (dict): Dictionary of SAM style tags, keys should match those given
            in minimap2 docs: https://lh3.github.io/minimap2/minimap2.html

    Returns:
    str:
        Tab separated string of tags in format 'tag:type:value'

    """
    return "\t".join("{}:{}:{}".format(k, REV_TYPES.get(k), v) for k, v in tags.items())


def _record_to_str(rec):
    """Convert PAF namedtuple to sting for output.

    Args:
        rec (namedtuple): PAF entry namedtuple, generated by read_paf.

    Returns:
        str: Tab separated string of PAF fields

    """
    return "\t".join([str(x) for x in rec[:-1]]) + "\t" + _tags_to_str(rec[-1]) + "\n"


def _paf_generator(file_like):
    """Generator that yields namedtuples from a PAF file.

    Args:
        file_like (file-like object): Generally an object with a read() method
            such as sys.stdin, a file handler from open() or io.StringIO.

    Yields:
        namedtuple: Correctly formatted PAF record and a dict of extra tags.

    """
    for rec in file_like:
        rec = rec.strip()
        if not rec:
            continue
        rec = rec.split("\t")
        yield Overlap(
            *(int(x) if x.isdigit() else x for x in rec[:12]), _parse_tags(rec[12:])
        )


def read_paf(filepath):
    """Read a minimap2 PAF file into a list.

    Args:
        filepath (str): Path to read PAF file from

    Returns:
        list: List of namedtuples

    """
    with open(filepath, "r") as fh:
        return list(_paf_generator(fh))


def write_paf(records, filepath):
    """Write a PAF file.

    Args:
        records (list): List of PAF namedtuples from read_paf.
        filepath (str): Path to write PAF file to.

    Returns:
        None

    """
    with open(filepath, "w") as fh:
        for rec in records:
            fh.write(_record_to_str(rec))
