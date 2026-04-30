CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    transport_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    non_compliance_count INT DEFAULT 0
);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL,
    incident_date DATE NOT NULL,
    high_visibility_vest BOOLEAN DEFAULT FALSE,
    safety_shoes BOOLEAN DEFAULT FALSE,
    no_badge BOOLEAN DEFAULT FALSE,
    not_following_yard_marshall_instructions BOOLEAN DEFAULT FALSE,
    exceeding_speed_loading_bay BOOLEAN DEFAULT FALSE,
    unnecessary_dwell_time BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
);