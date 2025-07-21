-- @author: Analytics Team
-- @purpose: Data warehouse reporting queries
-- @environment: production
-- @optimization_level: high

/*
@report_name: monthly_user_activity
@schedule: first_day_of_month
@recipients: management@company.com, analytics@company.com
@format: csv, pdf
@estimated_runtime: 45_minutes
@dependencies: users, user_sessions, user_activities
*/

WITH monthly_stats AS (
    SELECT 
        DATE_FORMAT(created_at, '%Y-%m') as month,
        COUNT(*) as new_users,
        COUNT(DISTINCT CASE WHEN last_login >= DATE_SUB(NOW(), INTERVAL 30 DAY) 
                           THEN id END) as active_users
    FROM users 
    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
)

-- @query_type: reporting
-- @cache_duration: 1_hour
-- @memory_requirement: medium
SELECT 
    month,
    new_users,
    active_users,
    ROUND((active_users / new_users) * 100, 2) as retention_rate
FROM monthly_stats
ORDER BY month DESC;

/*
@view_name: user_summary
@materialized: false
@refresh_frequency: real_time
@access_pattern: frequent
@security_level: internal
*/

CREATE VIEW user_summary AS
SELECT 
    u.id,
    u.username,
    u.email,
    CONCAT(p.first_name, ' ', p.last_name) as full_name,
    u.created_at as registration_date,
    COALESCE(s.last_activity, u.created_at) as last_seen
FROM users u
LEFT JOIN user_profiles p ON u.id = p.user_id
LEFT JOIN user_sessions s ON u.id = s.user_id;

-- @cleanup_task: true
-- @frequency: weekly  
-- @target: temporary_data
-- @retention: 30_days
DELETE FROM user_sessions 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
