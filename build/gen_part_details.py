import functools
import re

from dbconn import DbConnect

SQL_SELECT = """
SELECT part_num, name
  FROM parts
"""


@functools.cache
def get_overlay_regex():
    # WARNING: Never use numbers greater than 9 in the patterns below, the regex will break.
    regex_parts = []
    for pat in [
        r'^Technic .+ (#) ?([1-9][0-9]*)',
        r'^Technic Link 1 x `1+`',
        r'^Technic Brick 1 x `5+`',
        r'Axle ([4-9](?:\.[0-9])?)(?!\.)',
        r'Axle ([1-9][0-9]*(?:\.[0-9])?)(?!\.)(?! with)',
        r'Beam 1 x `5+`(?! Bent)',
        r'Tile `1+` x `1+`(?: with)?$',
        r'Tile Round `3+` x `3+`',
        r'^(?:Technic )?Plate...`4+` x 1',
        r'^(?:Technic )?Plate...1 x `4+`(?! Offset)(?! with)',
        r'^Plate...1 x `5+`',
        r'^(?:Technic )?Plate...`6+` x [1-6]',
        r'^(?:Technic )?Plate...[12] x `6+`',
        r'^Plate `2+` x `6+`',
        r'Wedge...`8+` x `1+`',
        r'Wedge Plate...`6+` x [1-3]',
        r'Dish `2+` x `2+`',
        r'Slope Curved `3+` x [12](?! Inverted)',
        r'Slope Curved [12] x `3+`(?! Inverted)',
        r'Slope(?! Curved)...`4+` x `1+`',
        r'Slope(?! Curved)...`1+` x `4+`',
        r'Panel 1 x `3+` x 1',
        r'Brick Round Corner, Curved `2+` x `2+` x ',
        r'Brick Round Corner `4+` x `4+`',
        r'Brick Curved `1+` x `4+`',
        r'Brick Curved `6+` x `1+`',
        r'^Brick `1+` x `5+`',
        r'Baseplate...`8+` x `8+`',
        r'(?:Hose|Bar|Cable)...([4-9]|[1-9][0-9]+)L',
        r'(?:Hose|Bar|Cable)...([2-9]|[1-9][0-9]+)L(?! with)',
    ]:
        pat = pat.replace('...', r'\b[^x]+\b')
        pat = re.sub(r'`([0-9]+)\+`', r'\\b([\1-9]|[1-9][0-9]+)\\b', pat)
        regex_parts.append(pat)

    return re.compile(r'\b(?:' + r'|'.join(regex_parts) + r')\b')


def find_overlay_from_part_name(part: str) -> str | None:
    part = re.sub(r' with .+', ' with', part)
    m = get_overlay_regex().search(part)
    if not m or ('Double' in part and 'Slope' in part) or 'LDU' in part or 'Modulex' in part:
        return None
    groups: list[str] = [g for g in m.groups() if g]
    prefix = ''
    if '#' in groups:
        prefix = '#'
        groups.remove('#')
    return prefix + max(groups, key=float)


def nat_sort_key(s):
    result = re.split(r"(0|[1-9][0-9]*)", s.lower())
    result[1::2] = map(int, result[1::2])
    return result


def gen_part_details(conn):
    print(":: generating part details ...")

    rows = list(conn.execute(SQL_SELECT))

    for col_i, dest_col in enumerate(('num_sort_pos', 'name_sort_pos')):
        rows.sort()
        rows.sort(key=lambda row: nat_sort_key(row[col_i]))
        with conn:
            conn.executemany(f'UPDATE parts SET {dest_col} = ? WHERE part_num = ?',
                             ((i, row[0]) for i, row in enumerate(rows, 1)))

    to_update = []
    for part_num, name in rows:
        if 'pr' in part_num or 'pat' in part_num:
            continue
        overlay = find_overlay_from_part_name(name)
        if overlay:
            to_update.append((overlay, part_num))
    with conn:
        conn.executemany(
            'UPDATE parts SET overlay = ? WHERE part_num = ?', to_update)


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_part_details(conn)
