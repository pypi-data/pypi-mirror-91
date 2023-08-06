import time

from kasten import Kasten, generator
from kasten.types import KastenPacked, KastenChecksum
from kasten.exceptions import InvalidID

from mimcvdf import vdf_create, vdf_verify

from onionrblocks.universalrules import check_block_sanity


class AnonVDFGenerator(generator.KastenBaseGenerator):
    @classmethod
    def get_ttl_seconds_per_rounds(cls, rounds: int):
        # 8000 rounds = 1 second (2.8ghz python) = 1 hour storage
        if rounds < 8000:
            raise ValueError(
                "Rounds must be at least 8000")
        return (rounds / 8000) * 60

    @classmethod
    def generate(
            cls, packed_bytes: KastenPacked, rounds: int = 5000) -> Kasten:
        return Kasten(
            vdf_create(
                packed_bytes,
                rounds, dec=True
                ).to_bytes(
                    64, "big"), packed_bytes, cls, auto_check_generator=False)

    @staticmethod
    def validate_id(
            hash: KastenChecksum,
            packed_bytes: KastenPacked, rounds=5000) -> None:

        try:
            hash = int.from_bytes(hash, byteorder="big")
        except TypeError:
            pass
        if not vdf_verify(packed_bytes, hash, rounds):
            raise InvalidID

        test_obj = Kasten(
            None, packed_bytes, None, auto_check_generator=False)
        allowed_age_seconds = AnonVDFGenerator.get_ttl_seconds_per_rounds(
            rounds)
        if time.time() > test_obj.get_timestamp() + allowed_age_seconds:
            raise ValueError(
                f"Block rounds only vaild through {allowed_age_seconds}")

        return None