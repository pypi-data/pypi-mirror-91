import os
import sys
import logging
import tarfile
import argparse
from typing import List
from storage_script.upload import upload_file


def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    upload_parser = subparsers.add_parser(
        "upload",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Uploads RASA models to AWS S3",
    )
    upload_parser.set_defaults(func=upload)

    set_upload_arguments(upload_parser)


def set_upload_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--model",
        "-m",
        required=True,
        type=str,
        help="Relative path to the Model (.tar.gz file)",
        default=None,
    )

    parser.add_argument(
        "--folder",
        "-f",
        required=False,
        type=str,
        help="Optional: Folder Name where the model needs to be saved in AWS S3",
        default="master",
    )


def upload(args: argparse.Namespace):

    if not os.path.exists(args.model):
        sys.exit(
            "Relative path {} does not exist! \n(for more information run the script with the --help option)".format(
                args.model
            )
        )
    elif not tarfile.is_tarfile(args.model):
        sys.exit(
            "The file {} to be uploaded is not a .tar.gz file. \nPlease upload a .tar.gz file.".format(
                args.model
            )
        )
    else:
        upload_file(args.model, args.folder)
