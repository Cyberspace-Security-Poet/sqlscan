LINUX = (
     "/var/www", "/usr/local/apache", "/usr/local/apache2", "/usr/local/www/apache22", "/usr/local/www/apache24",
    "/usr/local/httpd", "/var/www/nginx-default", "/srv/www", "/var/www/vhosts", "/opt/lampp",
    "/var/www/virtual", "/var/www/clients/vhosts", "/var/www/clients/virtual"
)

WINDOWS = (
     "/xampp", "/Program Files/xampp", "/wamp", "/Program Files/wampp", "/apache",
    "/Program Files/Apache Group/Apache",
    "/Program Files/Apache Group/Apache2", "/Program Files/Apache Group/Apache2.2",
    "/Program Files/Apache Group/Apache2.4", "/Inetpub/wwwroot",
    "/Inetpub/vhosts"
)

ALL = LINUX + WINDOWS

SUFFIXES = (
    "html", "htdocs", "httpdocs", "php", "public", "src", "site", 
    "build", "web", "www", "data", "sites/all", "www/build"
)