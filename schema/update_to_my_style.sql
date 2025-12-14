-- Additions

ALTER TABLE colors ADD COLUMN sort_pos INTEGER NOT NULL DEFAULT 0;
ALTER TABLE colors ADD COLUMN lightness REAL CHECK(lightness >= 0 AND lightness <= 1);

UPDATE colors
SET
  sort_pos = (SELECT sort_pos FROM color_properties WHERE id = colors.id),
  lightness = (SELECT lightness FROM color_properties WHERE id = colors.id),
  rgb = upper(rgb);

--

ALTER TABLE parts ADD COLUMN overlay TEXT CHECK (length(overlay) <= 3);
ALTER TABLE parts ADD COLUMN num_sort_pos INTEGER NOT NULL DEFAULT 0;
ALTER TABLE parts ADD COLUMN name_sort_pos INTEGER NOT NULL DEFAULT 0;
ALTER TABLE parts ADD COLUMN img_url TEXT;

UPDATE parts
SET
  img_url = (SELECT img_url FROM part_stats WHERE part_num = parts.part_num);

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
DROP TABLE part_rels_extra;
DROP VIEW color_stats;
DROP VIEW ___set_parts_for_stats;

--

VACUUM;
