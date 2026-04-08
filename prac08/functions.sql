-- functions.sql

-- 1. Search by pattern: name, surname, or phone
CREATE OR REPLACE FUNCTION search_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.last_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


-- 2. Pagination function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;