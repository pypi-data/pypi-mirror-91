# coding: utf8

import concurrent.futures
import functools
import logging
import pathlib

import click
import requests
from vgmusic.public import API

click.option = functools.partial(click.option, show_default=True)
_log = logging.getLogger("vgmusic.py")

LEVELS = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
]

logging.getLogger("urllib3").setLevel(logging.WARNING)

INDEX_FILENAME = "index.json"


def _download(url: str, dry_run: bool = False) -> None:
    if not dry_run:
        with requests.get(url) as response:
            return response.content


@click.command()
@click.option("-v", "--verbose", count=True, default=4, help="set verbosity (0-4)")
@click.option(
    "-n", "--no-download", is_flag=True, help="pretend to download files (dry run)"
)
@click.option(
    "-s",
    "--search",
    default="",
    help=(
        "filter specific songs using regex in the format "
        "'system_regex[::game_regex[::song_info_regex]]' "
    ),
)
@click.option(
    "-k", "--key", default="song_title", help="key to use to filter for song_info_regex"
)
@click.option(
    "-d",
    "--directory",
    default=".",
    help="where to download the midi files and the index.json file (song info) to",
)
def cli(verbose, no_download, search, key, directory):
    logging.basicConfig(level=LEVELS[verbose], format=" %(levelname)-8s :: %(message)s")

    directory = pathlib.Path(directory)
    index = directory / INDEX_FILENAME

    download_func = functools.partial(_download, dry_run=no_download)

    if not index.is_file():
        index.write_text("{}")

    _log.info("[download] starting")
    with API(index_path=index) as api:
        api.force_cache_all()

        songs = (
            (song["song_url"], directory / f"{song['song_title']}.mid")
            for song in api.search_by_regex(*search.split("::"), song_info_key=key)
        )

        with concurrent.futures.ThreadPoolExecutor() as pool:

            futures = {pool.submit(download_func, url): path for url, path in songs}
            for future in concurrent.futures.as_completed(futures):
                midi_path = futures[future]
                midi_data = future.result()

                _log.info("[download] %s", midi_path)

                with midi_path.open("wb") as f:
                    f.write(midi_data)


if __name__ == "__main__":
    cli()
