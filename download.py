#!/usr/bin/env python3
"""Download versioned CelloType resources from Zenodo using only Python's stdlib."""

import argparse
import hashlib
import http.client
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RECORD_URL = "https://zenodo.org/records/22736357"
ASSETS = {'example_codex_crc.zip': {'path': 'data/example_codex_crc.zip',
                           'bytes': 5710873605,
                           'sha256': '6e5a8436e129131bf8235586c6cd1a581bfc665a0999dc4927f07549118edaea'},
 'example_tissuenet.zip': {'path': 'data/example_tissuenet.zip',
                           'bytes': 1454315741,
                           'sha256': 'fa3bc6cbd6fb438ae7b589312d098a1e048e4aab826c5d4bc1e58554f03cb36e'},
 'example_xenium.zip': {'path': 'data/example_xenium.zip',
                        'bytes': 359151996,
                        'sha256': 'b18e6735d41d3974cd60434282ad054ea8be769a35f1dda48cbd800ae1246ea3'},
 'cellpose_model_0001999.pth': {'path': 'models/cellpose_model_0001999.pth',
                                'bytes': 2678352581,
                                'sha256': '6cdfa91d18902b51a80ebf62d1341ae3adfeaff29f356b2e9fda34443e071807'},
 'crc_model_0005999.pth': {'path': 'models/crc_model_0005999.pth',
                           'bytes': 2681633477,
                           'sha256': 'be3dfdd9107a4dd2cad68ae4dd3ecaf6480a2b3fe987ec9ddfe2c8c7266d0090'},
 'maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth': {'path': 'models/maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth',
                                                                                          'bytes': 895423421,
                                                                                          'sha256': '6ad634ffb2b7d802aa92312fd27e95c321c563b306744e0cff4aaa2394aaa8a2'},
 'tissuenet_model_0019999.pth': {'path': 'models/tissuenet_model_0019999.pth',
                                 'bytes': 2678352581,
                                 'sha256': '27bfa9bc719a4f1f2e2d10db830e5c1bf1fd39ce444ac8afe2366ff96630a75f'},
 'xenium_model_0001499.pth': {'path': 'models/xenium_model_0001499.pth',
                              'bytes': 2678352581,
                              'sha256': '11e3294a3edd72b960ad91303e3096196a45ce49765569186c65fd67d3b191ca'}}


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_asset(filename, output_root, base_url=RECORD_URL, attempts=5):
    """Return a verified local path, reusing complete files and resuming .part files."""
    asset = ASSETS[filename]
    destination = Path(output_root) / asset["path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and sha256_file(destination) == asset["sha256"]:
        print("Verified existing file: {}".format(destination))
        return destination
    partial = destination.with_name(destination.name + ".part")
    url = base_url.rstrip("/") + "/files/" + filename + "?download=1"
    for attempt in range(attempts):
        try:
            offset = partial.stat().st_size if partial.exists() else 0
            if offset >= asset["bytes"]:
                if offset == asset["bytes"] and sha256_file(partial) == asset["sha256"]:
                    partial.replace(destination)
                    return destination
                partial.unlink()
                offset = 0
            headers = {"User-Agent": "CelloType-resource-downloader/1.0"}
            if offset:
                headers["Range"] = "bytes={}-".format(offset)
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=60) as response:
                if response.status == 206:
                    content_range = response.headers.get("Content-Range", "")
                    if not content_range.startswith("bytes {}-".format(offset)):
                        raise OSError("Unexpected Content-Range: " + content_range)
                elif response.status == 200:
                    offset = 0  # This server may ignore Range; restart safely.
                else:
                    raise OSError("Unexpected HTTP status: {}".format(response.status))
                mode = "ab" if offset else "wb"
                last_report = 0.0
                with partial.open(mode) as stream:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        stream.write(chunk)
                        offset += len(chunk)
                        if offset > asset["bytes"]:
                            raise OSError("Response exceeds expected file size")
                        if time.monotonic() - last_report >= 1:
                            print("\r{}: {:.1f}%".format(filename, 100 * offset / asset["bytes"]), end="", flush=True)
                            last_report = time.monotonic()
            print()
            if partial.stat().st_size != asset["bytes"]:
                raise OSError("Incomplete transfer; partial file kept for resume")
            if sha256_file(partial) != asset["sha256"]:
                partial.unlink()
                raise OSError("SHA-256 mismatch; retrying from the start")
            partial.replace(destination)
            print("Verified: {}".format(destination))
            return destination
        except (OSError, urllib.error.URLError, http.client.IncompleteRead) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code in (401, 403, 404):
                raise RuntimeError("Zenodo returned HTTP {} for {}. Check service availability and the record URL: {}".format(error.code, filename, base_url)) from error
            if attempt + 1 == attempts:
                raise RuntimeError("Download failed for {}; rerun to resume any saved .part file".format(filename)) from error
            print("\nRetry {}/{}: {}".format(attempt + 1, attempts - 1, error), file=sys.stderr)
            time.sleep(min(2 ** attempt, 8))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="Exact filenames shown by --list; default: TissueNet checkpoint")
    parser.add_argument("--all", action="store_true", help="Download all eight assets (19.14 GB)")
    parser.add_argument("--list", action="store_true", help="List filenames and sizes without downloading")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent,
                        help="Directory containing models/ and data/ (default: this script's directory)")
    args = parser.parse_args()
    if args.list:
        for filename, asset in ASSETS.items():
            print("{:.2f} GB  {}".format(asset["bytes"] / 1e9, filename))
        return
    if args.all and args.files:
        parser.error("Choose --all or individual filenames")
    filenames = list(ASSETS) if args.all else (args.files or ["tissuenet_model_0019999.pth"])
    unknown = [name for name in filenames if name not in ASSETS]
    if unknown:
        parser.error("Unknown filename(s): " + ", ".join(unknown) + "; use --list")
    print("Record: " + RECORD_URL)
    print("File-specific licenses and attribution: " + RECORD_URL + "/files/LICENSES_AND_ATTRIBUTION.txt")
    if "example_tissuenet.zip" in filenames:
        print("TissueNet example data: non-commercial academic use under the upstream Modified Apache License.")
    try:
        for filename in dict.fromkeys(filenames):
            download_asset(filename, args.output_root)
    except (RuntimeError, OSError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
