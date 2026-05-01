from services.week_utils import get_operational_week
from datetime import date
from storage.database import Driver, Incident, db


class NonComplianceManager:
    @staticmethod
    def _find_driver(transporter_id=None, driver_name=None):
        if transporter_id:
            driver = Driver.query.filter_by(transport_id=transporter_id.strip()).first()
            if driver:
                return driver, None
            return None, "Driver not found for the selected Transporter ID. Please refresh the DA list."

        if driver_name:
            name = driver_name.strip()
            matches = Driver.query.filter(db.func.lower(Driver.name) == name.lower()).all()
            if len(matches) == 1:
                return matches[0], None
            if len(matches) > 1:
                return None, "Multiple drivers match that name. Please use Transporter ID."

        return None, "Driver not found. Check the DA list upload and spelling. Use Transporter ID for accuracy."

    def record_incident(
        self,
        transporter_id=None,
        driver_name=None,
        missing_vest=False,
        missing_shoes=False,
        no_badge=False,
        not_following_yard_marshall_instructions=False,
        exceeding_speed_loading_bay=False,
        unnecessary_dwell_time=False,
        incident_date=None,
    ):
        driver, error = self._find_driver(transporter_id=transporter_id, driver_name=driver_name)
        if error or not driver:
            return {
                "ok": False,
                "message": error or "Driver not found. Please refresh DA list and try again.",
            }

        if not any([
            missing_vest,
            missing_shoes,
            no_badge,
            not_following_yard_marshall_instructions,
            exceeding_speed_loading_bay,
            unnecessary_dwell_time,
        ]):
            return {"ok": False, "message": "Select at least one incident type."}

        incident = Incident(
            driver_id=driver.id,
            incident_date=incident_date,
            high_visibility_vest_missing=missing_vest,
            safety_shoes_missing=missing_shoes,
            no_badge=no_badge,
            not_following_yard_marshall_instructions=not_following_yard_marshall_instructions,
            exceeding_speed_loading_bay=exceeding_speed_loading_bay,
            unnecessary_dwell_time=unnecessary_dwell_time,
        )
        db.session.add(incident)

        driver.non_compliance_count += 1
        db.session.commit()

        incident_week = get_operational_week(incident_date)
        # determine weekly count for this driver (the week of the incident)
        weekly_count = Incident.query.filter(
            Incident.driver_id == driver.id,
            Incident.incident_date >= incident_week['week_start'],
            Incident.incident_date <= incident_week['week_end']
        ).count()
        escalation_needed = weekly_count >= 3
        message = (
            f"Incident recorded for {driver.name} (Transporter ID: {driver.transport_id}). "
            f"Non-Compliance Count: {driver.non_compliance_count}. Week {incident_week['week_number']} "
            f"({incident_week['week_start'].isoformat()} to {incident_week['week_end'].isoformat()})."
        )
        if escalation_needed:
            message += " User escalation to DSP is required."

        return {
            "ok": True,
            "message": message,
            "driver": driver,
            "escalation_needed": escalation_needed,
        }

    @staticmethod
    def get_escalation_drivers():
        # Return drivers who have 3 or more incidents in the current operational week, with weekly counts
        week = get_operational_week(date.today())
        week_start = week['week_start']
        week_end = week['week_end']

        # Aggregate by driver
        from storage.database import Incident
        escalations = []
        for d in Driver.query.order_by(Driver.name.asc()).all():
            count = Incident.query.filter(
                Incident.driver_id == d.id,
                Incident.incident_date >= week_start,
                Incident.incident_date <= week_end,
            ).count()
            if count >= 3:
                escalations.append({
                    'driver': d,
                    'weekly_count': count,
                })

        return escalations
