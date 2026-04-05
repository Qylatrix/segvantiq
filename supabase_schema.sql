-- SEGVANTIQ Database Schema
-- Run this in the Supabase SQL Editor to initialize your business accounts table.

CREATE TABLE IF NOT EXISTS businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    business_name TEXT NOT NULL,
    email TEXT,
    plan_tier TEXT DEFAULT 'Free',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;

-- Allow anonymous sign-up (if needed for public SaaS)
-- CREATE POLICY "Allow public sign-up" ON businesses FOR INSERT WITH CHECK (true);

-- Allow users to read only their own profile
CREATE POLICY "Users can view their own profile" 
ON businesses FOR SELECT 
USING (auth.uid()::text = id::text);

-- Create an index on username for fast login lookups
CREATE INDEX IF NOT EXISTS idx_businesses_username ON businesses(username);
