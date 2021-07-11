#! /usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime
from importlib.machinery import SourceFileLoader
from shutil import copyfile, rmtree

from public import os, toml, json, logger


# initialization of a timer to count the script execution time
timer = lambda: datetime.now().timestamp()
timer_start = timer()

# setting the workdir to the folder where this script is located
working_dir = os.path.dirname(os.path.abspath(__file__))

# parsing arguments passed to this script
options = ArgumentParser()
options.add_argument("-i", "--input",
                     help="the dir with distros for parsing",
                     default=f"{working_dir}/distros",
                     type=str)
options.add_argument("-o", "--output",
                     help="the dir for saving builded repo",
                     default=f"{working_dir}/../build",
                     type=str)

options = options.parse_args()

# setting other directories
output_dir = os.path.abspath(options.output)
distros_dir = os.path.abspath(options.input)

# initialization of arrays
repo, distros_errors = [], []
distros_list = sorted([distro for distro in os.listdir(distros_dir)
                       if not distro.startswith("_")])


def copy_distro_logo(distro_id):
    """Copy specific logo.png to distro folder."""
    try:
        copyfile(f"{distros_dir}/{distro_id}/logo.png",
                 f"{output_dir}/logos/{distro_id}.png")

    except FileNotFoundError:
        copyfile(f"{working_dir}/misc/fallback_logo.png",
                 f"{output_dir}/logos/{distro_id}.png")


def get_distro_info(distro_id):
    """Parse specific info.toml then return [distro name, distro url]."""
    try:
        target_toml = toml.load(f"{distros_dir}/{distro_id}/info.toml")
        distro_info = (target_toml["name"], target_toml["url"])
    except:
        fallback_url = "https://distrowatch.com/table.php?distribution={}"
        distro_info = [distro_id, fallback_url.format(distro_id)]

    return distro_info


def build_repo_entry(distro_id, distro_info):
    """Create a tulpe with distro values then return it."""

    target_file = f"{distros_dir}/{distro_id}/scraper.py"

    scraper = SourceFileLoader("scraper", target_file).load_module()

    repo_entry = {}
    repo_entry_releases = []

    repo_entry["id"] = distro_id
    repo_entry["name"] = distro_info[0]
    repo_entry["url"] = distro_info[1]

    distro_values = sorted(scraper.init(),
                           key=lambda x: x[3],
                           reverse=True)

    for distro_value in distro_values:
        iso_url, iso_arch, iso_size, iso_version = distro_value
        repo_entry_releases.append({"arch": iso_arch,
                                    "size": iso_size,
                                    "url": iso_url,
                                    "version": iso_version})

    repo_entry["releases"] = repo_entry_releases

    return repo_entry


if __name__ == "__main__":

    print(open(f"{working_dir}/misc/main_logo.txt", "r").read())

    try:
        logger("started scraping distros")
        for distro_id in distros_list:
            try:
                distro_info = get_distro_info(distro_id)

                # check if scraper.py exists in specific
                # distro folder, else skip current iteration
                if os.path.isfile(f"{distros_dir}/{distro_id}/scraper.py"):
                    repo_entry = build_repo_entry(distro_id, distro_info)
                    repo.append(repo_entry)
                    logger(f"{distro_id} is scraped", 0)
                else:
                    raise Exception("missing scraper.py")

            except Exception as error:
                distros_errors.append(distro_id)
                logger(f"{distro_id} is failed: {str(error).lower()}", 2)
                continue

        timer_stop = round(timer() - timer_start)

        if len(distros_errors) == len(distros_list):
            logger("the repository isn't built. check scrapers", 2)
            exit(2)

        # remove/create output folder structure
        os.remove(f"{output_dir}/repo.json")
        rmtree(f"{output_dir}/logos")
        os.makedirs(f"{output_dir}/logos", exist_ok=True)

        # create repo.json in output folder
        with open(f"{output_dir}/repo.json", "w") as repo_json:
            json.dump(repo, repo_json, indent=2)

        # copy distro logos to distro folders
        for distro_id in distros_list: copy_distro_logo(distro_id)

        logger(f"the repository is built in {timer_stop}s")

        if distros_errors:
            logger(f"not included: {', '.join(distros_errors)}")

        exit(0)

    except KeyboardInterrupt:
        exit(130)

    except Exception as error:
        logger(str(error).lower(), 2)
        exit(2)
