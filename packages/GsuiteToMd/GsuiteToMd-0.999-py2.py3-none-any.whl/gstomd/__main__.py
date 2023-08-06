# -*- coding: utf-8 -*-
import argparse
import logging

from gstomd.corpus import GsuiteToMd


def main():

    logger = logging.getLogger("gstomd")
    logger.debug("Start")
    folder_id = ""
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument(
        "--folder_id",
        action="store",
        type=str,
        required=True,
        help="Id of the folder to be converted",
    )
    my_parser.add_argument(
        "--folder_name",
        action="store",
        type=str,
        help="Name of the folder to be create created.",
        default="",
    )
    my_parser.add_argument(
        "--dest",
        action="store",
        help="destination root folder",
        default="gstomd_extract",
    )
    args = my_parser.parse_args()

    dest_folder_name = args.dest
    folder_id = args.folder_id
    folder_name = args.folder_name
    args = my_parser.parse_args()

    gstomd = GsuiteToMd(dest_folder=dest_folder_name)
    logger.debug("gsuiteTomd  Created")

    gstomd.Folder(
        folder_id=folder_id, root_folder_name=folder_name,
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
