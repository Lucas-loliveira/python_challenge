# python-challenge: Geo IP and RDAP lookups
Author: Lucas da Silva de Oliveira (lucasoliveira783@gmail.com, https://www.linkedin.com/in/lucas-sil-oliveira)

## Objective
Create a program in Python that will read a given set of IPs, perform Geo IP and RDAP lookups, and return the data back to the user.

Main technologies used:
  * python3
  * redis
  * docker
  * docker-compose
  * celery

Contents:
=================

<!--ts-->
   * [Requirements](#requirements)
   * [How to run the app](#how-to-run-the-app)
   * [Tests](#tests)
   * [Arquiteture](#arquiteture)
   * [GEOIP Service and API](#geoip-service-and-api)
   * [RDAP Service and API](#rdap-service-and-api)
   * [Future improvements](#future-improvements)

<!--te-->


Requirements
============
  * [docker](https://www.docker.com/)
  * [docker-compose](https://docs.docker.com/compose/)

How to run the app
============

run the containers and celery app
```bash
$ make build up celery
```
Expected result: 
![image](https://user-images.githubusercontent.com/22778168/189963428-b0a44549-5693-4b7e-a541-4e1dd55ef437.png)


Keep the last terminal open. 

Open a new terminal to execute the script that will perform Geo IP and RDAP lookups: 
```bash
$ make script
```
expected result: 
![image](https://user-images.githubusercontent.com/22778168/189963483-b182b035-c256-473e-94ac-4c1c5deeb835.png)

If you open the fist terminal, the terminal that is running the celery app you will start do see the logs of GEOIP and RDAP lookups:

![image](https://user-images.githubusercontent.com/22778168/189963519-876478ad-540c-4c08-a03c-96a108f1a34b.png)





Examples of the execution result can be seen in [result_data/result_geoip_example.txt](https://github.com/Lucas-loliveira/python_challenge/tree/main/result_data/result_geoip_example.txt) and [result_data/result_rdap_example.txt](https://github.com/Lucas-loliveira/python_challenge/tree/main/result_data/result_rdap_example.txt)




Stops containers and removes containers, networks, volumes, and images created: 

```bash
$ make down
```



Tests
=====

```bash
$ make test
```

Arquiteture
=====
![image](https://user-images.githubusercontent.com/22778168/189972856-a7cc8647-56ba-484a-bb2e-88d24123a1ca.png)



GEOIP Service and API
=====

To perform geoip searches I used the free api [ip-api](https://ip-api.com/). I used the [batch](https://ip-api.com/docs/api:batch) function that allows 100 ips to be processed per request.

However, the api has a limit of 15 requests per minute, so it was necessary to create a logic that waits until it is possible to make a new request. The implementation of this wait can be found in the src/geoip/ip_api_service.py file


RDAP Service and API
=====

To perform RDAP searches I used the free api [open RDAP](https://www.openrdap.org/api).

Unfortunately I didn't find any free api that provided a batch function like I found for GEOIP. Therefore, the performance of the RDAP module is very low since it is necessary to make an HTTP request for each ip. So to run the 5000 ips the service takes about 4 hours.

Future improvements
=====
  * Perform multiple asynchronous requests to the RDAP service to improve its performance
  * Replace prints with logs
  * CI
  * CD
  * Different environment variables for dev and production environments

