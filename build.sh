#! /bin/bash

set -eu

if [[ $# -gt 1 || $# -eq 1 && "$1" != "-rbonly" ]]; then
	echo -e "build.sh: invalid argument(s)\nusage: build.sh [-rbonly]" >&2
	exit 1
fi

which curl gzip python > /dev/null

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"
mkdir -p data

# Delete files if they are older than 1 day.
if find data -type f -mmin +1440 | grep -q .; then
	find data -type f -delete
fi

export PYTHONPATH=.
python build/download_api_data.py &
DOWNLOAD_API_DATA_PID=$!

TS="$(date +%s)"

for TABLE in {themes,colors,parts,part_{categories,relationships},elements,sets,minifigs,inventories,inventory_{parts,sets,minifigs}}.csv; do
	if [[ -f data/$TABLE ]]; then
		echo ":: skipped downloading (already exists) $TABLE"
	else
		echo ":: downloading $TABLE ..."
		curl -s "https://cdn.rebrickable.com/media/downloads/${TABLE}.gz?${TS}" | gzip -cd > "data/${TABLE}.part"
		mv "data/${TABLE}.part" "data/${TABLE}"
	fi
done

echo ":: $(python -m sqlite3 --version)"

echo ":: creating Rebrickable tables ..."

apply_sql() {
	python -c "import sqlite3; sqlite3.connect('data/rb.db').executescript(open('$1').read())"
}

rm -f data/rb.db
apply_sql schema/rb_tables.sql
apply_sql schema/api_tables.sql

python build/import_rb_tables.py

echo ":: creating indexes on Rebrickable tables ..."
apply_sql schema/rb_indexes.sql

if [[ $# -eq 0 ]]; then
	echo ":: creating custom tables ..."
	apply_sql schema/custom_tables.sql

	python build/gen_color_properties.py
	python build/gen_similar_color_ids.py
	python build/gen_part_rels_resolved.py

	echo ":: creating indexes on custom tables ..."
	apply_sql schema/custom_indexes.sql
fi

echo ":: making custom changes ..."
apply_sql schema/update_to_my_style.sql
python build/gen_alternate_parts.py
python build/gen_sort_orders.py

wait $DOWNLOAD_API_DATA_PID
python build/gen_api_tables.py

echo ":: running tests ..."
pytest -q tests tests

echo ":: done"
