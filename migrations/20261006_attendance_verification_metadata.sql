ALTER TABLE public.attendance_logs
    ADD COLUMN IF NOT EXISTS method text
        CHECK (method IS NULL OR method IN ('face', 'voice')),
    ADD COLUMN IF NOT EXISTS confidence double precision
        CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100));