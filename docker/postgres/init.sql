-- GT-Vision VMS - Database Initialization
-- Sprint 11 - Integration

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ADMIN CONTEXT
-- ============================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    permissions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User roles junction table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- ============================================
-- CIDADES CONTEXT
-- ============================================

-- Cidades table
CREATE TABLE IF NOT EXISTS cidades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    plano_retencao_dias INTEGER CHECK (plano_retencao_dias IN (7, 15, 30)),
    max_cameras INTEGER DEFAULT 1000,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Cameras table
CREATE TABLE IF NOT EXISTS cameras (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cidade_id UUID REFERENCES cidades(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    url_rtsp VARCHAR(500) NOT NULL,
    localizacao VARCHAR(500),
    status VARCHAR(20) DEFAULT 'INATIVA' CHECK (status IN ('ATIVA', 'INATIVA', 'ERRO')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cameras_cidade ON cameras(cidade_id);
CREATE INDEX IF NOT EXISTS idx_cameras_status ON cameras(status);

-- ============================================
-- STREAMING CONTEXT
-- ============================================

-- Streams table
CREATE TABLE IF NOT EXISTS streams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    camera_id UUID NOT NULL,
    source_url VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'STOPPED' CHECK (status IN ('STARTING', 'RUNNING', 'STOPPED', 'ERROR')),
    started_at TIMESTAMP,
    stopped_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_streams_camera ON streams(camera_id);
CREATE INDEX IF NOT EXISTS idx_streams_status ON streams(status);

-- Recordings table
CREATE TABLE IF NOT EXISTS recordings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stream_id UUID NOT NULL,
    retention_days INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'RECORDING' CHECK (status IN ('RECORDING', 'COMPLETED', 'FAILED')),
    started_at TIMESTAMP DEFAULT NOW(),
    stopped_at TIMESTAMP,
    storage_path VARCHAR(500),
    file_size_mb DECIMAL(10,2) DEFAULT 0,
    duration_seconds INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_recordings_stream ON recordings(stream_id);
CREATE INDEX IF NOT EXISTS idx_recordings_stopped_at ON recordings(stopped_at);
CREATE INDEX IF NOT EXISTS idx_recordings_status ON recordings(status);

-- Clips table
CREATE TABLE IF NOT EXISTS clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recording_id UUID NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
    storage_path VARCHAR(500),
    file_size_mb DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clips_recording ON clips(recording_id);
CREATE INDEX IF NOT EXISTS idx_clips_status ON clips(status);

-- Mosaics table
CREATE TABLE IF NOT EXISTS mosaics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    layout VARCHAR(20) DEFAULT '2x2' CHECK (layout IN ('1x1', '2x2', '3x3', '4x4')),
    camera_ids JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mosaics_user ON mosaics(user_id);

-- ============================================
-- AI CONTEXT
-- ============================================

-- LPR Events table
CREATE TABLE IF NOT EXISTS lpr_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    camera_id UUID NOT NULL,
    city_id UUID REFERENCES cidades(id) ON DELETE SET NULL,
    plate VARCHAR(8) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    image_url VARCHAR(500),
    detected_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_lpr_plate ON lpr_events(plate);
CREATE INDEX IF NOT EXISTS idx_lpr_camera ON lpr_events(camera_id);
CREATE INDEX IF NOT EXISTS idx_lpr_city ON lpr_events(city_id);
CREATE INDEX IF NOT EXISTS idx_lpr_detected_at ON lpr_events(detected_at);

-- ============================================
-- SEED DATA (Development)
-- ============================================

-- Insert default admin role
INSERT INTO roles (id, name, permissions) 
VALUES (
    uuid_generate_v4(),
    'ADMIN',
    '["users:read", "users:write", "cities:read", "cities:write", "cameras:read", "cameras:write"]'::jsonb
) ON CONFLICT (name) DO NOTHING;

-- Insert default viewer role
INSERT INTO roles (id, name, permissions)
VALUES (
    uuid_generate_v4(),
    'VIEWER',
    '["cameras:read", "streams:read", "recordings:read"]'::jsonb
) ON CONFLICT (name) DO NOTHING;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'GT-Vision VMS database initialized successfully!';
END $$;
