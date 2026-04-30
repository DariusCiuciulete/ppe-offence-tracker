class Driver:
    def __init__(self, transport_id, name):
        self.transport_id = transport_id
        self.name = name
        self.non_compliance_count = 0

    def add_non_compliance(self):
        self.non_compliance_count += 1

    def check_escalation(self):
        return self.non_compliance_count >= 3

    def __repr__(self):
        return f"Driver(transport_id={self.transport_id}, name={self.name}, non_compliance_count={self.non_compliance_count})"