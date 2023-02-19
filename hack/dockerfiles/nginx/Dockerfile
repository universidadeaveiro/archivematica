FROM archivematica-dashboard as dashboard-static

RUN yarn --cwd=/src/src/dashboard/frontend install --frozen-lockfile


FROM nginx:stable-alpine AS archivematica-nginx

# Django Static Files
COPY --from=dashboard-static /src/src/dashboard/src/media /static/dashboard
COPY ./hack/submodules/archivematica-storage-service/storage_service/static/ /static/storage-service

EXPOSE 80
EXPOSE 8000