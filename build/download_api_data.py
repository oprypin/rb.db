import contextlib
import csv
import itertools
import os
import os.path
import sys
import time
from typing import Callable, Iterator, Protocol

import rebrickable_api

UNKNOWN_COLOR_ID = -1
ANY_COLOR_ID = 9999


@contextlib.contextmanager
def atomicwrite(filename: str, mode='w', **kwargs):
    filename_part = filename + '.part'
    f = open(filename_part, mode, **kwargs)
    try:
        with f:
            yield f
    except Exception:
        os.unlink(filename_part)
        raise
    else:
        os.rename(filename_part, filename)


configuration = rebrickable_api.Configuration(
    api_key_prefix={"HeaderAuth": "key"},
    api_key={"HeaderAuth": os.environ["REBRICKABLE_API_KEY"]},
)
api_client = rebrickable_api.ApiClient(configuration)

lego_api = rebrickable_api.LegoApi(api_client)


class HttpResult[T](Protocol):
    results: list[T]
    next: str | None
    count: int


def paginate[**P, T](f: Callable[P, HttpResult[T]]) -> Callable[P, Iterator[T]]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> Iterator[T]:
        count = 0
        page = 1
        kwargs.setdefault("page_size", 999)
        while True:
            kwargs["page"] = page
            result = f(*args, **kwargs)
            count += len(result.results)
            yield from result.results
            print(f"{count} out of {result.count} done.", file=sys.stderr)
            if not result.next:
                break
            time.sleep(0.9)
            page += 1

    return inner


if not os.path.isfile('data/api_mapping_colors_bricklink_to_rebrickable.csv'):
    mapping: dict[int, list[tuple[bool, int]]] = {}

    for color in paginate(lego_api.list_colors)():
        if color.id in (UNKNOWN_COLOR_ID, ANY_COLOR_ID):
            continue
        if (bl := color.external_ids.brick_link) and (bl_ids := bl.ext_ids):
            for bl_id in bl_ids:
                if bl_id is not None and bl_id != color.id:
                    mapping.setdefault(bl_id, []).append((
                        color.name in itertools.chain(*bl.ext_descrs),
                        color.id
                    ))

    with atomicwrite('data/api_mapping_colors_bricklink_to_rebrickable.csv') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=('bricklink_id', 'color_id'))
        writer.writeheader()
        for bl_id, items in mapping.items():
            [color_id] = (
                color_id for (matches, color_id) in items if matches or len(items) == 1
            )
            writer.writerow(
                {'bricklink_id': bl_id, 'color_id': color_id}
            )

if not os.path.isfile('data/api_mapping_parts_bricklink_to_rebrickable.csv'):
    with atomicwrite('data/api_mapping_parts_bricklink_to_rebrickable.csv') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=('bricklink_id', 'part_num'))
        writer.writeheader()

        for color in paginate(lego_api.list_parts)():
            if bl_ids := color.external_ids.brick_link:
                for bl_id in bl_ids:
                    if bl_id is not None:
                        writer.writerow(
                            {'bricklink_id': bl_id, 'part_num': color.part_num}
                        )
