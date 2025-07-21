-- @author: Database Team
-- @version: 2.1.0
-- @description: Core database schema for user management
-- @category: schema
-- @priority: high
-- @dependencies: none

/*
@table_group: authentication
@created_date: 2024-01-10
@last_modified: 2024-07-21
@performance_requirements: high_throughput
@backup_frequency: hourly
@retention_policy: 7_years
*/

CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- @index_type: btree
-- @cardinality: high
-- @usage_pattern: frequent_lookups
CREATE INDEX idx_users_email ON users(email);

-- @index_type: btree
-- @cardinality: high
-- @usage_pattern: frequent_lookups
CREATE INDEX idx_users_username ON users(username);

/*
@table: user_profiles
@relationship: one_to_one
@foreign_key: user_id
@nullable_fields: bio, avatar_url, phone
@validation_required: true
*/

CREATE TABLE user_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    bio TEXT,
    avatar_url VARCHAR(500),
    phone VARCHAR(20),
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- @query_purpose: maintenance
-- @schedule: daily
-- @estimated_duration: 5_minutes
-- @impact: low
ANALYZE TABLE users, user_profiles;
