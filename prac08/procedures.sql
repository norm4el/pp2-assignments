-- procedures.sql

-- Optional: create table if it does not exist
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone VARCHAR(20) NOT NULL UNIQUE
);


-- 1. Upsert procedure:
-- if user with same first_name + last_name exists -> update phone
-- else insert new row
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_first_name
          AND COALESCE(last_name, '') = COALESCE(p_last_name, '')
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND COALESCE(last_name, '') = COALESCE(p_last_name, '');
    ELSE
        INSERT INTO contacts(first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$;


-- 2. Bulk insert procedure with validation
-- Uses arrays of names, surnames, phones
-- Invalid phones are saved into temp_invalid_contacts
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_first_names TEXT[],
    p_last_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    vv_first TEXT;
    vv_last TEXT;
    vv_phone TEXT;
BEGIN
    DROP TABLE IF EXISTS temp_invalid_contacts;

    CREATE TEMP TABLE temp_invalid_contacts (
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        reason TEXT
    ) ON COMMIT DROP;

    IF array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_phones, 1)
       OR array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_last_names, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1 .. array_length(p_first_names, 1)
    LOOP
        vv_first := p_first_names[i];
        vv_last := p_last_names[i];
        vv_phone := p_phones[i];

        -- Validation: only digits, optional leading +, length 10..15
        IF vv_phone IS NULL
           OR vv_phone !~ '^\+?[0-9]{10,15}$' THEN

            INSERT INTO temp_invalid_contacts(first_name, last_name, phone, reason)
            VALUES (vv_first, vv_last, vv_phone, 'Invalid phone format');

        ELSE
            -- Upsert logic
            IF EXISTS (
                SELECT 1
                FROM contacts
                WHERE first_name = vv_first
                  AND COALESCE(last_name, '') = COALESCE(vv_last, '')
            ) THEN
                UPDATE contacts
                SET phone = vv_phone
                WHERE first_name = vv_first
                  AND COALESCE(last_name, '') = COALESCE(vv_last, '');
            ELSE
                BEGIN
                    INSERT INTO contacts(first_name, last_name, phone)
                    VALUES (vv_first, vv_last, vv_phone);
                EXCEPTION
                    WHEN unique_violation THEN
                        INSERT INTO temp_invalid_contacts(first_name, last_name, phone, reason)
                        VALUES (vv_first, vv_last, vv_phone, 'Phone already exists');
                END;
            END IF;
        END IF;
    END LOOP;
END;
$$;


-- 3. Delete procedure by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$;