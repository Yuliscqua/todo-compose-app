FROM nginx:alpine

# Copier les fichiers du frontend dans le dossier web de Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY app.js /usr/share/nginx/html/app.js

# Exposer le port 80 dans le conteneur
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]