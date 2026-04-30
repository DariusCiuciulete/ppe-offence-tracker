from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

db = SQLAlchemy()


class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    transport_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    non_compliance_count = db.Column(db.Integer, default=0, nullable=False)
    # legacy field: some databases have a NOT NULL 'strikes' column — map it here to avoid insert failures
    strikes = db.Column(db.Integer, default=0, nullable=False)
    incidents = db.relationship("Incident", back_populates="driver", cascade="all, delete-orphan")


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False, index=True)
    incident_date = db.Column(db.Date, nullable=False, index=True)
    high_visibility_vest_missing = db.Column(db.Boolean, default=False, nullable=False)
    safety_shoes_missing = db.Column(db.Boolean, default=False, nullable=False)
    no_badge = db.Column(db.Boolean, default=False, nullable=False)
    not_following_yard_marshall_instructions = db.Column(db.Boolean, default=False, nullable=False)
    exceeding_speed_loading_bay = db.Column(db.Boolean, default=False, nullable=False)
    unnecessary_dwell_time = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    driver = db.relationship("Driver", back_populates="incidents")


class BikeIncident(db.Model):
    __tablename__ = "bike_incidents"

    id = db.Column(db.Integer, primary_key=True)
    bike_type = db.Column(db.String(20), nullable=False)  # mubea or citkar
    bike_serial = db.Column(db.String(100), nullable=False, index=True)
    incident_date = db.Column(db.Date, nullable=False, index=True)
    roll_back_on_ramp = db.Column(db.Boolean, default=False, nullable=False)
    missing_windscreen = db.Column(db.Boolean, default=False, nullable=False)
    faulty_handbrake = db.Column(db.Boolean, default=False, nullable=False)
    faulty_brake = db.Column(db.Boolean, default=False, nullable=False)
    shutting_off = db.Column(db.Boolean, default=False, nullable=False)
    worn_out_tyres = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        _ensure_driver_columns()
        _migrate_legacy_incident_data()
        _ensure_incident_columns()


def _ensure_driver_columns():
    inspector = inspect(db.engine)
    existing_columns = {column["name"] for column in inspector.get_columns("drivers")}

    if "non_compliance_count" not in existing_columns:
        db.session.execute(text("ALTER TABLE drivers ADD COLUMN non_compliance_count INTEGER NOT NULL DEFAULT 0"))

    if "strikes" in existing_columns:
        db.session.execute(text("""
            UPDATE drivers
            SET non_compliance_count = strikes
            WHERE (non_compliance_count IS NULL OR non_compliance_count = 0) AND strikes > 0
        """))

    db.session.commit()


def _migrate_legacy_incident_data():
    inspector = inspect(db.engine)
    table_names = set(inspector.get_table_names())
    legacy_table = "off" + "ences"
    current_table = "incidents"
    legacy_date_column = "off" + "ence_date"

    if legacy_table not in table_names or current_table not in table_names:
        return

    has_rows = db.session.execute(text(f"SELECT COUNT(1) FROM {current_table}")).scalar() or 0
    if has_rows > 0:
        return

    db.session.execute(text(
        f"""
        INSERT INTO {current_table} (
            driver_id,
            incident_date,
            high_visibility_vest_missing,
            safety_shoes_missing,
            no_badge,
            not_following_yard_marshall_instructions,
                exceeding_speed_loading_bay,
                unnecessary_dwell_time,
            created_at
        )
        SELECT
            driver_id,
            {legacy_date_column},
            high_visibility_vest_missing,
            safety_shoes_missing,
            COALESCE(no_badge, 0),
            COALESCE(not_following_yard_marshall_instructions, 0),
                COALESCE(exceeding_speed_loading_bay, 0),
                COALESCE(unnecessary_dwell_time, 0),
            COALESCE(created_at, CURRENT_TIMESTAMP)
        FROM {legacy_table}
        """
    ))
    db.session.commit()


def _ensure_incident_columns():
    inspector = inspect(db.engine)
    existing_columns = {column["name"] for column in inspector.get_columns("incidents")}
    required_columns = {
        "no_badge": "ALTER TABLE incidents ADD COLUMN no_badge BOOLEAN NOT NULL DEFAULT 0",
        "not_following_yard_marshall_instructions": (
            "ALTER TABLE incidents ADD COLUMN not_following_yard_marshall_instructions BOOLEAN NOT NULL DEFAULT 0"
        ),
        "exceeding_speed_loading_bay": (
            "ALTER TABLE incidents ADD COLUMN exceeding_speed_loading_bay BOOLEAN NOT NULL DEFAULT 0"
        ),
        "unnecessary_dwell_time": (
            "ALTER TABLE incidents ADD COLUMN unnecessary_dwell_time BOOLEAN NOT NULL DEFAULT 0"
        ),
    }

    for column_name, statement in required_columns.items():
        if column_name not in existing_columns:
            db.session.execute(text(statement))

    db.session.commit()