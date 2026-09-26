-- ====== YPDC PostgreSQL Schema ======
CREATE TABLE roles (id SERIAL PRIMARY KEY, name VARCHAR(30) UNIQUE NOT NULL);
INSERT INTO roles(name) VALUES ('student'),('member'),('directorate'),('faculty'),('admin'),('alumni');

CREATE TABLE users (
  id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(120) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, role_id INT REFERENCES roles(id), phone VARCHAR(20),
  status VARCHAR(20) DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW());

CREATE TABLE permissions (id SERIAL PRIMARY KEY, key VARCHAR(60) UNIQUE NOT NULL);
CREATE TABLE role_permissions (role_id INT REFERENCES roles(id), permission_id INT REFERENCES permissions(id), PRIMARY KEY(role_id, permission_id));

CREATE TABLE directorates (
  id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, description TEXT,
  director_id INT REFERENCES users(id), asst_director_id INT REFERENCES users(id),
  objectives TEXT, work_plan TEXT);

CREATE TABLE profiles (
  user_id INT PRIMARY KEY REFERENCES users(id), member_id VARCHAR(30) UNIQUE, roll_no VARCHAR(30),
  department VARCHAR(100), designation VARCHAR(100), directorate_id INT REFERENCES directorates(id),
  batch VARCHAR(10), company VARCHAR(100), position VARCHAR(100), skills TEXT, bio TEXT);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY, title VARCHAR(150) NOT NULL, description TEXT,
  assigned_to INT REFERENCES users(id), assigned_by INT REFERENCES users(id),
  directorate_id INT REFERENCES directorates(id), deadline DATE,
  status VARCHAR(20) DEFAULT 'pending', performance_score INT);

CREATE TABLE events (
  id SERIAL PRIMARY KEY, title VARCHAR(150) NOT NULL, description TEXT, type VARCHAR(50),
  event_date DATE, venue VARCHAR(150), budget NUMERIC, directorate_id INT REFERENCES directorates(id),
  proposed_by INT REFERENCES users(id), status VARCHAR(20) DEFAULT 'proposed',
  approved_by_faculty INT REFERENCES users(id), approved_by_admin INT REFERENCES users(id), created_at TIMESTAMP DEFAULT NOW());

CREATE TABLE event_registrations (
  id SERIAL PRIMARY KEY, event_id INT REFERENCES events(id), user_id INT REFERENCES users(id),
  role VARCHAR(20) DEFAULT 'participant', status VARCHAR(20) DEFAULT 'registered', UNIQUE(event_id, user_id));

CREATE TABLE attendance (
  id SERIAL PRIMARY KEY, event_id INT REFERENCES events(id), user_id INT REFERENCES users(id),
  marked_by INT REFERENCES users(id), method VARCHAR(10) DEFAULT 'manual', status VARCHAR(10) DEFAULT 'present',
  marked_at TIMESTAMP DEFAULT NOW());

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY, certificate_no VARCHAR(30) UNIQUE NOT NULL, user_id INT REFERENCES users(id),
  event_id INT REFERENCES events(id), title VARCHAR(150), pdf_url TEXT, issued_at TIMESTAMP DEFAULT NOW());

CREATE TABLE achievements (id SERIAL PRIMARY KEY, owner_type VARCHAR(20), owner_id INT, title VARCHAR(150), description TEXT, achieved_on DATE);
CREATE TABLE reports (id SERIAL PRIMARY KEY, directorate_id INT REFERENCES directorates(id), created_by INT REFERENCES users(id), title VARCHAR(150), content TEXT, file_url TEXT, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE documents (id SERIAL PRIMARY KEY, owner_type VARCHAR(20), owner_id INT, title VARCHAR(150), category VARCHAR(50), file_url TEXT, uploaded_at TIMESTAMP DEFAULT NOW());
CREATE TABLE notifications (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), message TEXT, type VARCHAR(20), read_at TIMESTAMP, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE feedback (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), event_id INT, type VARCHAR(20), rating INT, message TEXT, status VARCHAR(20) DEFAULT 'open', created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE applications (id SERIAL PRIMARY KEY, type VARCHAR(30), applicant_name VARCHAR(100), email VARCHAR(120), data JSONB, status VARCHAR(20) DEFAULT 'pending', reviewed_by INT, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE mentorships (id SERIAL PRIMARY KEY, mentor_id INT REFERENCES users(id), mentee_id INT REFERENCES users(id), area VARCHAR(100), status VARCHAR(20) DEFAULT 'active');
CREATE TABLE career_opportunities (id SERIAL PRIMARY KEY, title VARCHAR(150), company VARCHAR(100), type VARCHAR(30), location VARCHAR(100), posted_by INT, deadline DATE);
CREATE TABLE cms_content (id SERIAL PRIMARY KEY, page_key VARCHAR(50), title VARCHAR(150), content TEXT, media_url TEXT, updated_by INT, updated_at TIMESTAMP DEFAULT NOW());
