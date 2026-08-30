CREATE TABLE IF NOT EXISTS lab_status (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO lab_status (service_name, status)
VALUES ('secure-devops-app', 'online');
