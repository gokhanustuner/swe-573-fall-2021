# Community

To run the project on your local machine, please follow the instructions below;

Clone the repository
```
git clone git@github.com:gokhanustuner/swe-573-fall-2021.git
```

Go to project's root directory
```
cd swe-573-fall-2021
```

Build and run services and containers
```
docker-compose up -d –build
```

Go into the container
```
docker exec -ti swe578-web
```

Get static files into Django’s static file root path 
```
python manage.py collectstatic
```
