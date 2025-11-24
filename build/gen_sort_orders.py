import re

from dbconn import DbConnect


SQL_SELECT = """
SELECT part_num, name
  FROM parts
"""

def nat_sort_key(s):
    result = re.split(r"(0|[1-9][0-9]*)", s.lower())
    result[1::2] = map(int, result[1::2])
    return result


def gen_sort_orders(conn):
    print(":: generating sort orders ...")

    rows = list(conn.execute(SQL_SELECT))

    for col_i, dest_col in enumerate(('num_sort_pos', 'name_sort_pos')):
        rows.sort()
        rows.sort(key=lambda row: nat_sort_key(row[col_i]))
        with conn:
            conn.executemany(f'UPDATE parts SET {dest_col} = ? WHERE part_num = ?',
                            ((i, row[0]) for i, row in enumerate(rows, 1)))


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_sort_orders(conn)
