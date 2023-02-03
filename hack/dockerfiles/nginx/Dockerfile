FROM nginx:stable-alpine AS archivematica-nginx

# Django Static Files
COPY ../src/dashboard/src/static/ /static/dashboard
COPY ./submodules/archivematica-storage-service/storage_service/assets/ /static/storage-service

EXPOSE 80
EXPOSE 8000