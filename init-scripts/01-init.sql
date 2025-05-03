-- Initialize database with extensions and permissions

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Set up permissions
ALTER USER amazon WITH SUPERUSER;

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS amazon_tasks;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA amazon_tasks TO amazon;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA amazon_tasks TO amazon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA amazon_tasks TO amazon;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_task_status ON public.task(status);
CREATE INDEX IF NOT EXISTS idx_task_priority ON public.task(priority);
CREATE INDEX IF NOT EXISTS idx_task_user_id ON public.task(user_id);
CREATE INDEX IF NOT EXISTS idx_task_created_at ON public.task(created_at);

-- Set up database parameters for better performance
ALTER SYSTEM SET max_connections = '100';
ALTER SYSTEM SET shared_buffers = '128MB';
ALTER SYSTEM SET effective_cache_size = '512MB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET random_page_cost = '1.1';
ALTER SYSTEM SET effective_io_concurrency = '200';
ALTER SYSTEM SET wal_buffers = '4MB';
ALTER SYSTEM SET default_statistics_target = '100';
ALTER SYSTEM SET checkpoint_completion_target = '0.9';
ALTER SYSTEM SET autovacuum = 'on';