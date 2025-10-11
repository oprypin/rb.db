import math
from dbconn import DbConnect


SQL_RELS_LIST = """
SELECT *
  FROM part_relationships
 WHERE rel_type IN ('A', 'M')
"""


def gen_molds_resolved(conn):
    print(":: generating molds_resolved ...")

    rels = {}

    with conn:
        for rel_type, a, b in conn.execute(SQL_RELS_LIST):
            dist = {'M': 1, 'A': 10}[rel_type]
            rels[frozenset((a, b))] = dist

    while True:
        new_rels = {}
        for pair1, dist1 in rels.items():
            for pair2, dist2 in rels.items():
                xor = pair1 ^ pair2
                if len(xor) == 2:
                    if dist1 + dist2 < rels.get(xor, math.inf):
                        new_rels[xor] = dist1 + dist2
        if new_rels:
            rels.update(new_rels)
        else:
            break

    with conn:
        conn.executemany('INSERT INTO molds_resolved VALUES (?, ?, ?)',
                         ((a, b, dist) for (a, b), dist in rels.items()))
        conn.executemany('INSERT INTO molds_resolved VALUES (?, ?, ?)',
                         ((b, a, dist) for (a, b), dist in rels.items()))
        conn.executemany('INSERT INTO molds_resolved VALUES (?, ?, ?)',
                         ((a, a, dist) for (a, b), dist in rels.items()))
        conn.executemany('INSERT INTO molds_resolved VALUES (?, ?, ?)',
                         ((b, b, dist) for (a, b), dist in rels.items()))
        # A is not an alternative to B
        for pair in [
            ('3788', '60212'),
            {'3749', '43093'},
            {'3673', '2780'},
            ('3063a', '3063b'),
            ('6069', '48933'),
            {'3730', '63082'},
            {'32556', '6558'},
            {'4868b', '4868a'},
            ('40666', '10661'),
            ('85861', '6141'),
            {'3705b', '3705'},
            ('3795', '32001'),
            ('3020', '3709'),
            ('3034', '3738'),
            ('3062a', '3062b'),
        ]:
            a, b = pair
            conn.execute("DELETE FROM molds_resolved WHERE part_a = ? AND part_b = ?", (b, a))
            if isinstance(pair, set):
                conn.execute("DELETE FROM molds_resolved WHERE part_a = ? AND part_b = ?", (a, b))


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_molds_resolved(conn)
