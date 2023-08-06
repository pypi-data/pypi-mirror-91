import os
import sys
import logging
import argparse
import tarfile
from typing import List
from storage_script.download import download_file


def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    download_parser = subparsers.add_parser(
        "download",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Downloads RASA models from AWS S3",
    )
    download_parser.set_defaults(func=download)

    set_download_arguments(download_parser)


def set_download_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--model",
        "-m",
        required=True,
        type=str,
        help="Model Name(.tar.gz file)",
        default=None,
    )

    parser.add_argument(
        "--folder",
        "-f",
        required=False,
        type=str,
        help="Optional: Folder Name from where the model needs to be downloaded",
        default="master",
    )


def download(args: argparse.Namespace):

    if not args.model.endswith(".tar.gz"):
        sys.exit(
            "The file {} to be downloaded is not a .tar.gz file. \nPlease enter a .tar.gz file.".format(
                args.model
            )
        )
    else:
        download_file(args.model, args.folder)
