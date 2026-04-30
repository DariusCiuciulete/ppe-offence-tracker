import pandas as pd
from storage.database import Driver, db


def _load_file(file_obj):
    filename = getattr(file_obj, 'filename', '') or ''
    if filename.lower().endswith('.csv'):
        return pd.read_csv(file_obj)
    return pd.read_excel(file_obj)


def _resolve_column(df, accepted_names):
    for column_name in df.columns:
        normalized = str(column_name).strip().lower()
        if normalized in accepted_names:
            return column_name
    return None


def import_excel(file_obj):
    """Import DA list (Excel or CSV) and merge by Transporter ID, preserving existing non-compliance counts."""
    df = _load_file(file_obj)

    transport_column = _resolve_column(df, {"transporter id"})
    name_column = _resolve_column(df, {"driver name", "name"})

    if not transport_column or not name_column:
        raise ValueError("File must include columns: 'Transporter ID' and 'Driver Name'.")

    added = 0
    updated = 0
    skipped = 0

    for _, row in df.iterrows():
        transport_id = str(row.get(transport_column, "")).strip()
        driver_name = str(row.get(name_column, "")).strip()

        if not transport_id or transport_id.lower() == "nan" or not driver_name or driver_name.lower() == "nan":
            skipped += 1
            continue

        driver = Driver.query.filter_by(transport_id=transport_id).first()
        if driver is None:
            db.session.add(Driver(transport_id=transport_id, name=driver_name))
            added += 1
        else:
            if driver.name != driver_name:
                driver.name = driver_name
                updated += 1

    db.session.commit()

    return {
        "total_rows": len(df.index),
        "added": added,
        "updated": updated,
        "skipped": skipped,
    }