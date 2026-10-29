WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY crm_customer_id
            ORDER BY updated_at DESC
        ) AS row_number
    FROM {{ source('silver', 'customers') }}
)
SELECT
    crm_customer_id,
    LOWER(TRIM(email)) AS email,
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') AS phone,
    state,
    marketing_consent::boolean AS marketing_consent,
    created_at::timestamptz AS created_at,
    updated_at::timestamptz AS updated_at
FROM ranked
WHERE row_number = 1
