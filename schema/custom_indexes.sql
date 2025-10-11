CREATE INDEX similar_color_ids_ref_id_idx ON similar_color_ids(ref_id);

CREATE UNIQUE INDEX part_color_stats_part_num_color_id_idx ON part_color_stats(part_num, color_id);

CREATE UNIQUE INDEX part_rels_resolved_rel_type_child_part_num_idx ON part_rels_resolved(rel_type, child_part_num);
CREATE INDEX part_rels_resolved_rel_type_parent_part_num_idx ON part_rels_resolved(rel_type, parent_part_num);

CREATE INDEX molds_resolved_part_a_idx ON molds_resolved(part_a);

CREATE UNIQUE INDEX part_rels_extra_rel_type_child_part_num_idx ON part_rels_extra(rel_type, child_part_num);
