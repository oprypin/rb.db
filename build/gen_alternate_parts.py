import math
import re
from dbconn import DbConnect


SQL_RELS_LIST = """
SELECT *
  FROM part_relationships
 WHERE rel_type IN ('A', 'M')
"""
SQL_PRINTS_LIST = """
SELECT *
  FROM part_relationships
 WHERE rel_type IN ('P', 'T')
"""

def _excluded_pairs():
    result = set()
    for pair in [
        # A is not an alternative to B
        ('3788', '60212'),
        {'3749', '43093'},
        {'3673', '2780'},
        ('3063a', '3063b'),
        ('6069', '48933'),
        {'3730', '63082'},
        {'32556', '6558'},
        {'4868b', '4868a'},
        ('40666', '10661'),
        ('6141', '85861'),
        {'3705b', '3705'},
        ('3795', '32001'),
        ('3020', '3709'),
        ('3034', '3738'),
        ('3062a', '3062b'),
    ]:
        a, b = pair
        result.add((b, a))
        if isinstance(pair, set):
            result.add((a, b))
    return frozenset(result)


def is_excluded_pair(a, b, excluded_pairs=_excluded_pairs(), regex=re.compile('^(.+?)(?:pr.+|pat.+|)$')):
    return (regex.search(a)[1], regex.search(b)[1]) in excluded_pairs



def gen_alternate_parts(conn):
    print(":: generating alternate_parts ...")

    rels = {}

    with conn:
        for rel_type, a, b in conn.execute(SQL_RELS_LIST):
            dist = {'M': 1, 'A': 10}[rel_type]
            if not is_excluded_pair(a, b):
                rels[(a, b)] = dist
            if not is_excluded_pair(b, a):
                rels[(b, a)] = dist

    while True:
        new_rels = {}
        for (a, b), dist1 in rels.items():
            for (c, d), dist2 in rels.items():
                if b == c and a != d:
                    if not is_excluded_pair(a, d):
                        if dist1 + dist2 < rels.get((a, d), math.inf):
                            new_rels[(a, d)] = dist1 + dist2
        if new_rels:
            rels.update(new_rels)
        else:
            break

    for rel_type, a, b in conn.execute(SQL_PRINTS_LIST):
        rels[(a, b)] = 100

    with conn:
        conn.executemany('INSERT INTO alternate_parts VALUES (?, ?, ?)',
                         ((a, a, 0) for a in {a for (a, _) in rels}))
        conn.executemany('INSERT INTO alternate_parts VALUES (?, ?, ?)',
                         ((a, b, dist) for (a, b), dist in rels.items()))


if __name__ == '__main__':
    with DbConnect() as conn:
        gen_alternate_parts(conn)
