-- Additions

ALTER TABLE colors ADD COLUMN sort_pos INTEGER NOT NULL DEFAULT 0;

UPDATE colors
SET sort_pos = (
  SELECT color_properties.sort_pos
  FROM color_properties
  WHERE color_properties.id = colors.id
);

UPDATE colors
SET rgb = upper(rgb);

--

CREATE TABLE alternate_parts(
  part_a TEXT NOT NULL REFERENCES parts(part_num),
  part_b TEXT NOT NULL REFERENCES parts(part_num),
  distance INTEGER CHECK(distance >= 0)
) STRICT;

CREATE INDEX alternate_parts_part_a_idx ON alternate_parts(part_a);

-- Removals from rb.db

DROP TABLE color_properties;
DROP TABLE similar_color_ids;
DROP VIEW similar_colors;
DROP TABLE part_rels_resolved;
DROP TABLE part_rels_extra;
DROP VIEW part_stats;
DROP VIEW color_stats;
DROP VIEW ___set_parts_for_stats;

--

VACUUM;
