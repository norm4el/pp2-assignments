CREATE OR REPLACE PROCEDURE add_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    vv_group_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO vv_group_id
    FROM groups
    WHERE name = p_group_name;

    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
    VALUES (p_first_name, p_last_name, p_email, p_birthday, vv_group_id);
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    vv_contact_id INT;
BEGIN
    SELECT id INTO vv_contact_id
    FROM contacts
    WHERE first_name = p_contact_name
    LIMIT 1;

    IF vv_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
    ELSE
        INSERT INTO phones(contact_id, phone, type)
        VALUES (vv_contact_id, p_phone, p_type);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    vv_group_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO vv_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = vv_group_id
    WHERE first_name = p_contact_name;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_value TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR id IN (
            SELECT contact_id
            FROM phones
            WHERE phone = p_value
       );
END;
$$;