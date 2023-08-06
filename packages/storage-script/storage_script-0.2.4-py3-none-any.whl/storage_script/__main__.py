import os
import sys
import logging
import argparse
from os import environ
import boto3
import threading
from botocore.exceptions import ClientError
from storage_script import __version__ as storage_script_version
from storage_script.cli import (
    upload,
    download,
)


def create_argument_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="Storage Script - Command line interface that uploads/downloads RASA models to/from AWS S3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        "-v",
        help="Package Version",
        action="version",
        version=storage_script_version,
    )

    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parsers = [parent_parser]

    subparsers = parser.add_subparsers(help="Rasa Storage Commands")

    upload.add_subparser(subparsers, parents=parent_parsers)
    download.add_subparser(subparsers, parents=parent_parsers)

    return parser


def main() -> None:
    checkEnvVariables()
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    if hasattr(cmdline_arguments, "func"):
        cmdline_arguments.func(cmdline_arguments)
    elif hasattr(cmdline_arguments, "version"):
        print_version()
    else:
        arg_parser.print_help()
        exit(1)


def checkEnvVariables():
    for data in [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
        "AWS_S3_BUCKET_RASA_MODELS",
    ]:
        env_var = os.environ.get(data)
        if not env_var:
            raise ValueError("Environment variable %s not set" % data)


if __name__ == "__main__":
    main()
