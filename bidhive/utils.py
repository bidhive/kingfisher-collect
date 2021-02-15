# Bidhive defined utils
import os
from os.path import isfile, isdir
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


class ItemManager:
    def __init__(self):
        self.items = []

    def set_items(self, items: list):
        self.items = items


def format_release(release: dict):
    print(release.get("ocid"))


def format_item(item_json: str):
    item = json.loads(item_json)
    return item


def read_dir(path: str, dir_name: str):
    final_dir_path = f"{path}/{dir_name}"

    files = os.listdir(final_dir_path)

    items = []
    for file in files:
        file_name = f"{final_dir_path}/{file}"
        with open(file_name, "r") as file:
            items.append(format_item("\n".join(file.readlines())))

    return items


import itertools


def read_dirs(path: str):
    if not isdir(path):
        raise ValueError("Path is not a directory")

    directories = os.listdir(path)
    all_items = []

    only_read_first = True
    if only_read_first:
        directories = [directories[0]]

    for directory in directories:
        all_items.append(read_dir(path, directory))

    flat_iterable = itertools.chain.from_iterable(all_items)
    return list(flat_iterable)
