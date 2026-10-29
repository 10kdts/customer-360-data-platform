WITH order_metrics AS (
    SELECT
        crm_customer_id,
        COUNT(DISTINCT order_id) FILTER (WHERE status = 'completed') AS order_count,
        COALESCE(SUM(total_amount) FILTER (WHERE status = 'completed'), 0) AS lifetime_value,
        MAX(ordered_at) FILTER (WHERE status = 'completed') AS last_purchase_at
    FROM {{ source('silver', 'orders') }}
    GROUP BY crm_customer_id
),
support_metrics AS (
    SELECT
        crm_customer_id,
        COUNT(*) AS support_ticket_count,
        AVG(satisfaction_score) AS average_satisfaction
    FROM {{ source('silver', 'support_tickets') }}
    GROUP BY crm_customer_id
)
SELECT
    customer.crm_customer_id AS customer_id,
    customer.state,
    customer.marketing_consent,
    COALESCE(orders.order_count, 0) AS order_count,
    COALESCE(orders.lifetime_value, 0) AS lifetime_value,
    orders.last_purchase_at,
    COALESCE(support.support_ticket_count, 0) AS support_ticket_count,
    support.average_satisfaction
FROM {{ ref('stg_customers') }} AS customer
LEFT JOIN order_metrics AS orders USING (crm_customer_id)
LEFT JOIN support_metrics AS support USING (crm_customer_id)
