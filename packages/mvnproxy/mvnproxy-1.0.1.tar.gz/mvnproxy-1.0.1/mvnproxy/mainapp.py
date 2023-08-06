import hashlib
import io
import os
from xml.etree.ElementTree import ElementTree
import textwrap

import addict
import flask
import requests
import termcolor_util
import yaml
from flask import send_file

# this must be read like this, not with a __main__ section
from mvnproxy.maven_metadata_merger import merge_maven_metadata, xml_to_string
from mvnproxy import config

os.makedirs(config.cache_folder, exist_ok=True)

app = flask.Flask("mvnproxy")


@app.route("/", methods=["GET"])
def index_page():
    return send_file("../static/index.html")


# @app.route('/repo/<path:path>', methods=['HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
# def not_implemented(path: str) -> None:
#     print(termcolor_util.red(f"Unable to process {path}: unsupported method"))
#     raise Exception("not implemented")


@app.route("/repo/<path:path>", methods=["GET"])
def maven_file(path: str):
    try:
        if is_cached(path):
            return send_file(cache_path(path))

        print(f"processing non-cached: {path}")

        if path.endswith(".sha1"):
            compute_sha1_checksum(path)
        elif path.endswith("/maven-metadata.xml"):
            construct_maven_metadata(path)
        else:
            download_from_remotes(path)

        return send_file(cache_path(path))
    except Exception as e:
        print(termcolor_util.red(f"Unable to process {path}: {e}"))
        raise e


def is_cached(path: str) -> bool:
    return os.path.isfile(cache_path(path))


def cache_path(path: str) -> str:
    return os.path.join(config.cache_folder, path)


def compute_sha1_checksum(path: str) -> None:
    # we remove the .sha1 suffix
    file_path = cache_path(path)
    with open(file_path[:-5], "rb") as input_file:
        with open(file_path, "wt") as output_file:
            sha_1 = hashlib.sha1()
            sha_1.update(input_file.read())
            output_file.write(sha_1.hexdigest())
            output_file.write("\n")


def construct_maven_metadata(path: str) -> None:
    artifact_folder = cache_path(os.path.dirname(path))
    os.makedirs(artifact_folder, exist_ok=True)

    known_xmls = []

    for mirror in config.data.mirrors:
        print(f"Trying to fetch {mirror.url}{path}")
        auth = None

        if mirror.auth:
            auth = (mirror.auth["user"], mirror.auth["pass"])

        r = requests.get(f"{mirror.url}{path}", auth=auth)

        if not r.ok:
            print(f"{mirror.url} failed to resolve {path}: {r}")
            continue

        known_xmls.append(ElementTree(file=io.BytesIO(r.content)))

    out_xml = merge_maven_metadata(known_xmls)

    with open(cache_path(path), "wt", encoding="utf-8") as f:
        f.write(xml_to_string(out_xml))


def download_from_remotes(path) -> None:
    artifact_folder = cache_path(os.path.dirname(path))
    os.makedirs(artifact_folder, exist_ok=True)

    for mirror in config.data.mirrors:
        print(f"Trying to fetch {mirror.url}{path}")
        auth = None

        if mirror.auth:
            auth = (mirror.auth["user"], mirror.auth["pass"])

        r = requests.get(f"{mirror.url}{path}", auth=auth)

        if not r.ok:
            if r.status_code == 401:
                print(
                    termcolor_util.red(
                        f"401 UNAUTHORIZED: {mirror.url} failed to resolve {path}: {r}"
                    )
                )
            if r.status_code == 403:
                print(
                    termcolor_util.red(
                        f"403 FORBIDDEN: {mirror.url} failed to resolve {path}: {r}"
                    )
                )
            else:
                print(
                    termcolor_util.yellow(f"{mirror.url} failed to resolve {path}: {r}")
                )

            continue

        with open(cache_path(path), "wb") as f:
            f.write(r.content)

        return
