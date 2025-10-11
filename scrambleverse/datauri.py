from urllib.parse import urlparse, unquote
import base64
from typing import NamedTuple


__all__ = ["parse_data_uri", "ParsedDataURI"]


class ParsedDataURI(NamedTuple):
    mime_type: str
    data: bytes


def parse_data_uri(data_uri: str):
    parsed = urlparse(data_uri)
    if parsed.scheme != "data":
        raise ValueError("Not a data URI")

    # Split the path into metadata and data
    metadata, _, data = parsed.path.partition(",")
    if not data:
        raise ValueError("No data found in the URI")

    # Default values
    mime_type = "text/plain;charset=US-ASCII"
    is_base64 = False

    if ";" in metadata:
        i = metadata.rindex(";")
        parts = (metadata[:i], metadata[i + 1 :])
        mime_type = parts[0] if parts[0] else mime_type
        is_base64 = "base64" in parts[1:]
    elif metadata:
        mime_type = metadata

    # TODO: maximum length check for data

    # Decode the data
    if is_base64:
        byte_data = base64.b64decode(data)
    else:
        byte_data = unquote(data).encode("utf-8")

    return ParsedDataURI(mime_type, byte_data)
