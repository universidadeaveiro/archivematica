SERVICE="archivematica-dashboard"

URL="${URL:-http://archivematica-dashboard-service:8000}"

ORGANIZATION_ID="${ORGANIZATION_ID:-test}"
ORGANIZATION_NAME="${ORGANIZATION_NAME:-test}"

SUPERUSER_USERNAME="${SUPERUSER_USERNAME:-test}"
SUPERUSER_PASSWORD="${SUPERUSER_PASSWORD:-test}"
SUPERUSER_EMAIL="${SUPERUSER_EMAIL:-test@test.com}"
SUPERUSER_API_KEY="${SUPERUSER_API_KEY:-test}"

STORAGE_SERVICE_URL="${STORAGE_SERVICE_URL:-http://archivematica-storage-service-service:8000}"
STORAGE_SERVICE_SUPERUSER_USERNAME="${STORAGE_SERVICE_SUPERUSER_USERNAME:-test}"
STORAGE_SERVICE_SUPERUSER_API_KEY="${STORAGE_SERVICE_SUPERUSER_API_KEY:-test}"

sh kubectl-run-command.sh $SERVICE \
		/src/src/dashboard/src/manage.py \
            migrate --noinput

sh kubectl-run-command.sh $SERVICE  \
		/src/src/dashboard/src/manage.py \
            install \
                --username="$SUPERUSER_USERNAME" \
                --password="$SUPERUSER_PASSWORD" \
                --email="$SUPERUSER_EMAIL" \
                --org-name="$ORGANIZATION_NAME" \
                --org-id="$ORGANIZATION_ID" \
                --api-key="$STORAGE_SERVICE_SUPERUSER_API_KEY" \
                --ss-url="$STORAGE_SERVICE_URL" \
                --ss-user="$STORAGE_SERVICE_SUPERUSER_USERNAME" \
                --ss-api-key="$SUPERUSER_API_KEY" \
                --site-url="$URL"