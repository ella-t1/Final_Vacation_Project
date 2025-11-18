-- Vacations project schema - Complete DDL with constraints and seed data

-- Drop tables in reverse order of dependencies (for clean reset)
DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS vacations CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- 1. Roles table
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(32) UNIQUE NOT NULL,
  CONSTRAINT check_role_name CHECK (name IN ('Admin', 'User'))
);

-- 2. Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  username VARCHAR(100),
  role_id INTEGER NOT NULL,
  CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
);

-- 3. Countries table
CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

-- 4. Vacations table
CREATE TABLE vacations (
  id SERIAL PRIMARY KEY,
  country_id INTEGER NOT NULL,
  description TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  image_name VARCHAR(255),
  CONSTRAINT fk_vacations_country FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE RESTRICT,
  CONSTRAINT check_price_range CHECK (price >= 0 AND price <= 10000),
  CONSTRAINT check_dates CHECK (end_date >= start_date)
);

-- 5. Likes table (composite primary key)
CREATE TABLE likes (
  user_id INTEGER NOT NULL,
  vacation_id INTEGER NOT NULL,
  CONSTRAINT pk_likes PRIMARY KEY (user_id, vacation_id),
  CONSTRAINT fk_likes_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_likes_vacation FOREIGN KEY (vacation_id) REFERENCES vacations(id) ON DELETE CASCADE
);

-- Seed data

-- Insert roles
INSERT INTO roles (name) VALUES 
  ('Admin'),
  ('User')
ON CONFLICT (name) DO NOTHING;

-- Insert countries (at least 10 real countries)
INSERT INTO countries (name) VALUES
  ('United States'),
  ('France'),
  ('Italy'),
  ('Spain'),
  ('Greece'),
  ('Japan'),
  ('Thailand'),
  ('Australia'),
  ('Brazil'),
  ('Mexico'),
  ('Egypt'),
  ('Turkey')
ON CONFLICT (name) DO NOTHING;

-- Insert users (Admin and User)
-- Note: Passwords are plain text for now (in production, use bcrypt/hashing)
INSERT INTO users (first_name, last_name, email, password, username, role_id) VALUES
  ('Admin', 'User', 'admin@vacations.com', 'admin1234', 'admin', 1),
  ('John', 'Doe', 'john@example.com', 'user1234', 'johndoe', 2)
ON CONFLICT (email) DO NOTHING;

-- Insert vacations (at least 12 vacations with logical data)
INSERT INTO vacations (country_id, description, start_date, end_date, price, image_name) VALUES
  (2, 'Romantic Paris getaway with Eiffel Tower visit', CURRENT_DATE + INTERVAL '30 days', CURRENT_DATE + INTERVAL '37 days', 2500.00, 'paris.jpg'),
  (3, 'Beautiful Italian Riviera experience', CURRENT_DATE + INTERVAL '45 days', CURRENT_DATE + INTERVAL '52 days', 3200.00, 'italy.jpg'),
  (4, 'Sunny Barcelona beach vacation', CURRENT_DATE + INTERVAL '60 days', CURRENT_DATE + INTERVAL '67 days', 1800.00, 'barcelona.jpg'),
  (5, 'Ancient Greek islands tour', CURRENT_DATE + INTERVAL '75 days', CURRENT_DATE + INTERVAL '82 days', 2100.00, 'greece.jpg'),
  (6, 'Tokyo cultural immersion experience', CURRENT_DATE + INTERVAL '90 days', CURRENT_DATE + INTERVAL '97 days', 4500.00, 'tokyo.jpg'),
  (7, 'Tropical Thailand paradise', CURRENT_DATE + INTERVAL '15 days', CURRENT_DATE + INTERVAL '22 days', 1500.00, 'thailand.jpg'),
  (8, 'Sydney and Great Barrier Reef adventure', CURRENT_DATE + INTERVAL '120 days', CURRENT_DATE + INTERVAL '127 days', 3800.00, 'australia.jpg'),
  (9, 'Rio de Janeiro carnival experience', CURRENT_DATE + INTERVAL '105 days', CURRENT_DATE + INTERVAL '112 days', 2800.00, 'brazil.jpg'),
  (10, 'Cancun beach resort vacation', CURRENT_DATE + INTERVAL '20 days', CURRENT_DATE + INTERVAL '27 days', 2200.00, 'mexico.jpg'),
  (11, 'Pyramids and Nile cruise', CURRENT_DATE + INTERVAL '135 days', CURRENT_DATE + INTERVAL '142 days', 1900.00, 'egypt.jpg'),
  (12, 'Istanbul cultural tour', CURRENT_DATE + INTERVAL '50 days', CURRENT_DATE + INTERVAL '57 days', 1600.00, 'turkey.jpg'),
  (1, 'New York City urban adventure', CURRENT_DATE + INTERVAL '100 days', CURRENT_DATE + INTERVAL '107 days', 3500.00, 'nyc.jpg')
ON CONFLICT DO NOTHING;

-- Likes table starts empty (as per requirements)

