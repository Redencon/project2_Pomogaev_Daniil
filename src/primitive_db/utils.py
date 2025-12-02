"""Utility functionsx"""
import json

DEFAULT_META_FILE = "db_meta.json"


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, metadata):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)