SERVICE="archivematica-storage-service"

SUPERUSER_USERNAME="${SUPERUSER_USERNAME:-test}"
SUPERUSER_PASSWORD="${SUPERUSER_USERNAME:-test}"
SUPERUSER_EMAIL="${SUPERUSER_USERNAME:-test@test.com}"
SUPERUSER_API_KEY="${SUPERUSER_USERNAME:-test}"

sh kubectl-run-command.sh $SERVICE \
		/src/storage_service/manage.py \
            migrate --noinput

sh kubectl-run-command.sh $SERVICE  \
		/src/storage_service/manage.py \
            create_user \
                --username="$SUPERUSER_USERNAME" \
                --password="$SUPERUSER_PASSWORD" \
                --email="$SUPERUSER_EMAIL" \
                --api-key="$SUPERUSER_API_KEY" \
                --superuser