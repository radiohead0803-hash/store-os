# Live Commerce API Operations

Use this only after CSV staging and dry-run payload validation pass.

## Supported staging targets
- Naver SmartStore staging CSV/API payload.
- Coupang product/order/shipping staging CSV/API payload.
- Shopify product import and draft publishing payload.

## Required controls
- Secrets stored only in deployment secret managers.
- Webhook signature verification for order/payment/shipping callbacks.
- Idempotency keys for product, order, and shipping updates.
- Audit logs for every external action.
- Rollback plan for price, stock, visibility, and product text changes.
- Operator approval ID included in every live publish/update action.

## CS and order loop
1. Import orders with `ingest-orders`.
2. Review `fulfillment_queue.csv`.
3. Review `cs_triage.csv`; escalation messages cannot be auto-sent.
4. Stage shipping updates in `shipping_update_staging.csv`.
5. Only after approval should a platform-specific adapter call live endpoints.

## Image loop
1. Run `image-plan`.
2. Generate candidate images in the chosen image tool.
3. Run readability, claims, and IP checks.
4. Store source log and approval record.
5. Use image only after operator approves public use.
