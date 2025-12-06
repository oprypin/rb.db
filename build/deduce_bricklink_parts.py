import csv
import json
import xml.etree.ElementTree as etree
from typing import Mapping


def get_mapping_from_xml(filename: str) -> Mapping[int, str]:
    root = etree.parse(filename).getroot()
    return {
        int(next(obj for obj in item if obj.tag == "ITEMID").text or ""):
        next(obj for obj in item if obj.tag == "MINQTY").text or ""
        for item in root
    }


def get_mapping_from_csv(filename: str) -> Mapping[int, str]:
    with open(filename) as f:
        return {int(item['Quantity']): item['Part'] for item in csv.DictReader(f)}


def main():
    mapping_xml = get_mapping_from_xml(
        'data/rebrickable_parts_bricklink_unknown_parts.xml')
    mapping_csv = get_mapping_from_csv(
        'data/rebrickable_parts_bricklink_unknown_parts.csv')

    mapping = {
        mapping_xml[key]: mapping_csv[key]
        for key in mapping_xml.keys() & mapping_csv.keys()
    }
    with open('utils/mapping_parts_bricklink_to_rebrickable.json', 'w') as f:
        json.dump(mapping, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
