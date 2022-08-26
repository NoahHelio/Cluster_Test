# Getting Started

Run locally with docker compose:
```
$ docker compose up --build
# 
# LOTS of text as docker pulls the images and 
# builds the next steps, and then launches the 
# containers.  Finally you'll see...
cluster_test-service_demo-1  |  * Debugger PIN: 642-840-851

# Next, get the ingress service's port from docker ps
$ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED              STATUS              PORTS                                           NAMES
e78d383b9a47   cluster_test_ingress_demo   "python3 main.py"        About a minute ago   Up About a minute   0.0.0.0:49161->54321/tcp, :::49161->54321/tcp   cluster_test-ingress_demo-1
a2848f2bb16e   cluster_test_service_demo   "python3 main.py"        About a minute ago   Up About a minute   12345/tcp                                       cluster_test-service_demo-1
ef1cf4c0ba39   cluster_test_psql           "docker-entrypoint.s…"   7 minutes ago        Up About a minute   5432/tcp                                        cluster_test-psql-1

```

Then visit http://localhost:[PORT]/ (The port is 49161 in this example) in your browser to visit the ingress pod and test db, service, and service-to-db connections. 

The ingress pod serves a page like this:   
>     
>  Ingress pod is reachable and responsive!   
>     
>  Other links:   
>  _Service connection_   
>  _Database connection_    
>  _Test service db connection_ (these are clickable links when served)   

