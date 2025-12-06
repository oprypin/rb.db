import csv

from dbconn import DbConnect


def gen_api_tables(conn):
    print(":: generating API tables ...")

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
    with conn:
        for bricklink_id, part_nums in mapping.items():
            if len(part_nums) == 1:
                if bricklink_id != part_nums[0]:
                    conn.execute('''
                        INSERT INTO bricklink_to_rebrickable_parts (bricklink_id, part_num)
                        VALUES (?, ?)
                    ''', (bricklink_id, part_nums[0]))
                continue

            stmt = '''
                INSERT INTO bricklink_to_rebrickable_parts (bricklink_id, part_num)
                SELECT %r, sub.part_num
                FROM (
                    SELECT part_num
                    FROM part_stats
                    WHERE part_num IN %r
                    ORDER BY max_year DESC, num_parts DESC, min_year DESC, part_num DESC
                    LIMIT 1
                ) AS sub;
            ''' % (bricklink_id, tuple(part_nums))
            conn.execute(stmt)
        conn.execute(
            'DELETE FROM bricklink_to_rebrickable_parts WHERE bricklink_id = part_num'
        )


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_api_tables(conn)
