from basic_colormath.distance import get_delta_e_hex
from contextlib import closing
from dbconn import DbConnect


MAX_DELTA_E = 20
UNKNOWN_COLOR_ID = -1
ANY_COLOR_ID = 9999

SQL_CROSS_COLORS = f"""
WITH
  part_colors AS (
    SELECT DISTINCT part_num, color_id
    FROM inventory_parts
    WHERE color_id NOT IN ({UNKNOWN_COLOR_ID}, {ANY_COLOR_ID})
  ),
  color_pairs AS (
    SELECT DISTINCT pc1.color_id id1, pc2.color_id id2
    FROM part_colors pc1
    JOIN part_colors pc2 ON pc1.part_num = pc2.part_num
  )
SELECT id1, c1.rgb, id2, c2.rgb
FROM color_pairs
JOIN colors c1 ON c1.id = id1
JOIN colors c2 ON c2.id = id2;
"""


def gen_similar_color_ids(conn):
    print(":: generating similar_color_ids ...")

    id_pairs = []
    all_ids = set()
    with closing(conn.cursor()) as cur:
        for id1, rgb1, id2, rgb2 in cur.execute(SQL_CROSS_COLORS):
            if get_delta_e_hex(rgb1, rgb2) <= MAX_DELTA_E:
                id_pairs.append((id1, id2))
            all_ids.add(id1)
    id_pairs.extend((ANY_COLOR_ID, id2) for id2 in all_ids)

    with conn, closing(conn.cursor()) as cur:
        cur.executemany('INSERT INTO similar_color_ids VALUES (?, ?)', id_pairs)


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_similar_color_ids(conn)
