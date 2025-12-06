import csv
import json
from typing import Mapping

from dbconn import DbConnect


def gen_api_tables(conn):
    print(":: generating API tables ...")

    with open('utils/mapping_parts_bricklink_to_rebrickable.json') as f:
        known_mapping_from_bricklink: Mapping[str, str] = json.load(f)

    with conn:
        conn.execute('DELETE FROM bricklink_to_rebrickable_colors')
        conn.execute('DELETE FROM bricklink_to_rebrickable_parts')

    with open('data/api_mapping_colors_bricklink_to_rebrickable.csv') as f, conn:
        conn.executemany(
            'INSERT INTO bricklink_to_rebrickable_colors (bricklink_id, color_id) VALUES (:bricklink_id, :color_id)',
            csv.DictReader(f),
        )

    mapping: dict[str, list[str]] = {}
    with open('data/api_mapping_parts_bricklink_to_rebrickable.csv') as f:
        for row in csv.DictReader(f):
            mapping.setdefault(row['bricklink_id'], []).append(row['part_num'])
    with conn, open('data/rebrickable_parts_bricklink_unknown_parts.xml', 'w') as f:
        print('<INVENTORY>', file=f)
        i = 0

        for bricklink_id, part_nums in sorted(mapping.items()):
            if len(part_nums) > 1:
                [(count,)] = conn.execute(
                    "SELECT coalesce(sum(num_parts), 0) FROM part_stats WHERE part_num IN %r" %
                    (tuple(part_nums),)
                )
                if count > 20:
                    i += 1
                    print(
                        f'<ITEM>'
                        f'<ITEMTYPE>P</ITEMTYPE>'
                        f'<ITEMID>{bricklink_id}</ITEMID>'
                        f'<COLOR>1</COLOR>'
                        f'<MINQTY>{i}</MINQTY>'
                        f'</ITEM>',
                        file=f
                    )

            if bricklink_id in known_mapping_from_bricklink:
                part_nums = [known_mapping_from_bricklink[bricklink_id]]

            if len(part_nums) == 1:
                if bricklink_id != part_nums[0]:
                    conn.execute('''
                        INSERT INTO bricklink_to_rebrickable_parts (bricklink_id, part_num)
                        SELECT ?, ?
                        WHERE EXISTS (
                            SELECT 1 FROM parts WHERE part_num = ?
                        );
                    ''', (bricklink_id, part_nums[0], part_nums[0]))
                continue

            stmt = '''
                INSERT INTO bricklink_to_rebrickable_parts (bricklink_id, part_num)
                SELECT %s, sub.resolved_part_num
                FROM (
                    SELECT coalesce(part_rels_resolved.parent_part_num, part_num) AS resolved_part_num
                    FROM part_stats
                    LEFT JOIN part_rels_resolved ON part_rels_resolved.rel_type = 'M' AND part_rels_resolved.child_part_num = part_stats.part_num
                    WHERE part_num IN (%s)
                    ORDER BY max_year DESC, num_parts DESC, min_year DESC, part_num DESC
                    LIMIT 1
                ) AS sub;
            ''' % (repr(bricklink_id), repr(list(part_nums))[1:-1])
            conn.execute(stmt)

        conn.execute(
            'DELETE FROM bricklink_to_rebrickable_parts WHERE bricklink_id = part_num'
        )
        print('</INVENTORY>', file=f)


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_api_tables(conn)
