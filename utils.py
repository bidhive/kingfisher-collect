# Bidhive defined utils
import os
from os.path import isfile, isdir
import sys
import json

# Release format
# ocid: string
# id: string
# date: string
# initiationType: string
# language: string
# parties: {
#   id: string
#   name: string
#   additionalIdentifiers: {
#       id: string
#       scheme: string
#   }[]
#   address: {
#       streetAddress: string
#       locality: string
#       region: string
#       postalCode: string
#       countryName: Australia
#       contactPoint: {
#           name: string
#           telephone: string
#           branch: string
#           division: string
#           roles: string[]
#           id: string
#       }
#       roles: string[]
#   }
# }[]
# awards: {
#   id: string
#   suppliers: {
#       id: string
#       name: string
#   }[]
#   status: string
#   date: string
# }[]
# contracts: array
# tag: string[]
# tender: {
#   id: string
#   procurementMethod: string
#   procurementMethodDetails: string
# }


def format_release(release: dict):
    print(release.get("ocid"))


def format_item(item_json: str):
    item = json.loads(item_json)
    # for key in item.keys():
    #     if key != "releases":
    #         print(item.get(key))
    # print(item.keys())

    print_details = False
    if print_details:
        print("URI: " + item.get("uri"))
        print("Publisher: " + item.get("publisher").get("name"))
        print("Published at: " + item.get("publishedDate"))
        print("Licence: " + item.get("license"))
        print("Version: " + item.get("version"))
        # print("Releases: " + item.get("releases"))
        print("Extensions: " + "".join(item.get("extensions")))
        # print("Links: " + item.get("links"))

    releases = item.pop("releases")
    for release in releases:
        format_release(release)


def read_dir(path: str, dir_name: str):
    final_dir_path = f"{path}/{dir_name}"

    files = os.listdir(final_dir_path)
    for file in files:
        file_name = f"{final_dir_path}/{file}"
        with open(file_name, "r") as file:
            format_item("\n".join(file.readlines()))


def read_dirs(path: str):
    if not isdir(path):
        raise ValueError("Path is not a directory")

    directories = os.listdir(path)

    only_read_first = True
    if only_read_first:
        directories = [directories[0]]

    for directory in directories:
        read_dir(path, directory)


if __name__ == "__main__":
    read_dirs("data/australia_sample")
