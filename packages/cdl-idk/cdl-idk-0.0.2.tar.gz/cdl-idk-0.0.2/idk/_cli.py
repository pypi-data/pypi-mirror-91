#! python3

import argparse
import io
import json
import os
import pprint
import re
import shutil
import sys
import uuid
import zipfile

import requests

from ._service import _service_url
from ._utils import get_logger
from ._version import __version__

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

logger = get_logger()


def _get_insight_name():
    # Regex extract alphabeticals and stick them back together snake case
    dr = str(os.path.basename(os.getcwd()))
    words = re.findall("[a-zA-Z]+", dr)
    return "_".join(word.lower() for word in words)


def _init():
    """method describes what happens when someone runs idk init in folder"""

    # Check folder is empty
    if len(os.listdir(os.getcwd())) != 0:
        logger.error("A new insight can only be started in a empty directory.")
        sys.exit(1)
    # Check if folder name is short enough -
    # basically if it's smaller than the max size of insihgtg generator id - hash

    # Check folder name is alphabetical with addition of "-" "_"

    logger.info("Creating Insight directory structure...")
    insight_name = _get_insight_name()
    if len(insight_name) == 0:
        logger.error(
            "The alphabetical letters in your file is used to create your insight name. You need at least 1 letter."
        )
        sys.exit(1)

    insight_file = "{}.py".format(insight_name)

    with open(insight_file, "w+") as f:
        with open(os.path.dirname(__file__) + "/_resources/_template.py", "r") as tmpl:
            class_name = insight_name.title().replace("_", "")
            f.write(tmpl.read().replace("_DeveloperInsight_", class_name))

    with open("idk.json", "w+") as config_file:
        config = {
            "insight_name": insight_name,
            "insight_file": insight_file,
        }
        json.dump(config, config_file, indent=4)

    with open("requirements.txt", "w+") as req:
        req.writelines([
            "# Add your requirements here. You can add the packages in your currrent python environemnt with:",
            "#     pip freeze > requirements.txt",
            "idk",
        ]
        )

    # - Make .env file for python virtual environment?

    logger.info("READY! Happy coding!")


def _get_create_hashname():
    cwd = os.getcwd()
    out_path = cwd + "/idk.out/out.json"

    if os.path.exists(out_path):
        # Check if hashname in file
        with open(out_path, "r") as out_file:
            out = json.load(out_file)
            if "hashname" in out:
                return out["hashname"]

        # If not then make one
        with open(cwd + "/idk.json", "r") as config:
            config = json.load(config)
            out["hashname"] = config["insight_name"] + str(uuid.uuid4().hex)

        with open(out_path, "w") as out_file:
            out_file.write(json.dumps(out, indent=4))

    else:  # if no outfile exists
        with open(cwd + "/idk.json", "r") as config:
            config = json.load(config)

        out = {"hashname": config["insight_name"] + str(uuid.uuid4().hex)}

        with open(out_path, "w+") as out_file:
            out_file.write(json.dumps(out, indent=4))

    return out["hashname"]


def _validate_base_directory():
    cwd = os.getcwd()
    if not os.path.exists(cwd + "/idk.json"):
        sys.exit("No idk.json in current working directory, are you in the base directory of your insight?")


def _deploy(test):
    """Define What happends when someone runs idk deploy in a folder
    """
    cwd = os.getcwd()
    _validate_base_directory()

    # Check and make output dir
    outdir = cwd + "/idk.out"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    hashname = _get_create_hashname()

    # Zip the folder
    zip_path = outdir + "/{}.zip".format(hashname)
    with zipfile.ZipFile(zip_path, mode="w", compression=compression) as outzip:
        # add devs files
        for root, _, f_names in os.walk(cwd):
            if root.endswith("idk.out"):
                continue
            for f in f_names:
                dir_ = root.replace(cwd, "")
                if len(dir_) != 0:
                    path = dir_[1:] + "/" + f
                    outzip.write(path, path, compress_type=compression)
                else:
                    outzip.write(f, compress_type=compression)

        # add buildspec
        outzip.write(
            os.path.dirname(__file__) + "/_resources/buildspec.yaml",
            "buildspec.yaml",
            compress_type=compression,
        )

        pprint.pprint(outzip.infolist())

    with open(zip_path, "rb") as outfile:
        out_data = outfile.read()

    params = {"hashname": hashname}
    data = {
        "zfile": out_data
    }

    with zipfile.ZipFile(io.BytesIO(data["zfile"]), "r") as nz:
        pprint.pprint(nz.infolist())

    # Upload to cloud
    # Can get user credential from:
    # os.path.expanduser("~") + /.idk/crednetials?
    # with requests.post(_service_url + "insight", params=params, data=data) as response:
    #     if response.ok:
    #         logger.info("Success! Your insight is deployed to the insight engine! Deploy again to update.\n" +
    #                     json.loads(response.content)
    #                     )
    #     else:
    #         logger.error("Unable to deploy your insight:\n" + json.loads(response.content))


def _get_hashname():
    out_path = os.getcwd() + "/idk.out/out.json"

    if os.path.exists(out_path):
        # Check if hashname in file
        with open(out_path, "r") as out_file:
            out = json.load(out_file)
            if "hashname" in out:
                return out["hashname"]
        logger.error(
            "Could not find \"hashname\" in {}. Are you sure you've deployed this insight before?".format(out_path)
        )
    logger.error("Could not find {}. Are you sure you've deployed this insight before?".format(out_path))
    sys.exit(1)


def _destroy(test):
    """Code that runs when a user wants to delete their insight.
    """

    _validate_base_directory()

    # with requests.delete(_service_url + "insight", params={"hashname": _get_hashname()}) as response:
    #     print(json.loads(response.content))

    # When we destroy we will need to delete the hashkey in order to make a new one next time it's deployed?
    # Probably yes for safety reasons (no risk of accidentally not deleting a lambda functions somewhere and)
    # THIS SHOULD DEFINITELY ONLY RUN IF WE'RE SURE ALL THE OTHER SERVICES HASVE DELETED THEIR PARTS.
    shutil.rmtree(os.getcwd() + "/idk.out")


def main():
    parser = argparse.ArgumentParser(
        prog="CDL Insights Development Kit (cdl_idk)",
        description="A toolkit to help you build and deploy impactful insights for the CDL Insights Engine."
    )
    parser.add_argument("--init", action="store_true",
                        help="creates a new insight project in the current empty directory")
    parser.add_argument("--deploy", action="store_true",
                        help="deploys or updates your insight to CDL Insights Engine")
    parser.add_argument("--destroy", action="store_true",
                        help="tears down you insight from CDL Insight Engine")
    parser.add_argument("-t", "--test", action="store_true",
                        help="for developer use only")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    if args.init:
        if args.test:
            logger.warning("test flag has no affect on init command")
        _init()
    elif args.deploy:
        _deploy(args.test)
    elif args.destroy:
        _destroy(args.test)
    else:
        logger.error("Please pass one of init, deploy, or destroy arguments.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
