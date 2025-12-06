CREATE TABLE bricklink_to_rebrickable_colors(
  bricklink_id INTEGER NOT NULL PRIMARY KEY,
  color_id INTEGER NOT NULL REFERENCES colors(id)
) STRICT;

CREATE TABLE bricklink_to_rebrickable_parts(
  bricklink_id TEXT NOT NULL PRIMARY KEY,
  part_num TEXT NOT NULL REFERENCES parts(part_num)
) STRICT;
