from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from services.non_compliance_manager import NonComplianceManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

non_compliance_manager = NonComplianceManager()


@app.route('/incident', methods=['GET', 'POST'])
def incident_form():
    if request.method == 'POST':
        transporter_id = request.form.get('transport_id')
        driver_name = request.form.get('driver_name')
        high_visibility_vest = 'high_visibility_vest' in request.form
        safety_shoes = 'safety_shoes' in request.form
        incident_date = request.form.get('incident_date')

        if transporter_id or driver_name:
            non_compliance_manager.record_incident(
                transporter_id=transporter_id,
                driver_name=driver_name,
                missing_vest=high_visibility_vest,
                missing_shoes=safety_shoes,
                incident_date=datetime.strptime(incident_date, '%Y-%m-%d').date() if incident_date else None,
            )
            flash('Incident recorded successfully!', 'success')
            return redirect(url_for('incident_form'))

        flash('Please enter either Transporter ID or Driver Name.', 'error')

    return render_template('incident_form.html')
