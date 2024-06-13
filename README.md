# Celes Challenge

This project was developed in order to provide a solution to the technical test that consists of developing a microservice in Python that interacts with a Datamart and provides an interface to perform specific queries and operations. In addition, the microservice should integrate authentication with Firebase and have a focus on unit testing and CI/CD.

## How to start?🚀

_These instructions will allow you to get a copy of the project up and running on your local machine for development and testing purposes._

### Installation 🔧

First we must clone the repository, access the folder and then create a virtual environment to install all the necessary libraries.

```
git clone https://github.com/jsdnlb/celes-challenge.git
cd celes-challenge
python3 -m venv venv # Create virtual environment
source venv/bin/activate # Activate environment, may vary in other os
```

Once the environment is active we can install requirements

```
pip install -r requirements.txt
```

Create the .env and serviceAccountKey.json files that were shared in the mail, add the data folder with the .parquet files to the root of the project

With this we would have everything necessary to run the project and see the magic.

```
uvicorn main:app --reload
```

![image](https://github.com/jsdnlb/celes-challenge/assets/17171887/29403a99-e915-42e0-9fb9-ecb2ae45e6ff)

## Running endpoints 🔐

Just enter the documentation [Swagger](http://localhost:8000/docs#/) to start using it you can simply use the test user that is by default in the enpoint **/api/users/signup/** or you can simply create a new user to perform your tests, obviously this endpoint does not have any kind of protection to facilitate the process, this in production would be catastrophic for our application.

The first time you consume the endpoint it will take a little while to read the whole files and generate the session using pyspark, the second consumption of any endpoint will be faster because we will already have the information loaded and ready to operate.

Once the user is created you can log in by clicking on the authorize button should show you something like the figure below, or simply selecting the padlock of any protected enpoint you can log in, once you have entered your credentials the token will expire in an hour, with that you can use all the endpoints.

![image](https://github.com/jsdnlb/celes-challenge/assets/17171887/42510a48-0fb9-4c45-8268-d6f03465b639)

## Running tests ⚙️

To run one of the tests found in the tests/ folder

```
python -m unittest discover -s tests
```
![image](https://github.com/jsdnlb/celes-challenge/assets/17171887/84f3b4f0-a626-4238-9772-1846f9b08ae9)

## Built with 🛠️

_This project was built with the following tools_

* [Python](https://www.python.org/) - Programming language
* [FastAPI](https://fastapi.tiangolo.com/) - Framework
* [Firebase](https://firebase.google.com/docs/auth/) - Authentication
* [Unittest](https://docs.python.org/3/library/unittest.html) - Unit testing framework
* [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) - Large-Scale data processing

## Wiki 📖

Once you have the project running you can run it in a simple way here: [Swagger](http://localhost:8000/docs#/) and find the documentation in a more visual way here [OpenAPI](http://localhost:8000/redoc) , although in theory both have the same information.

## Things to improve 🌟

* Include users in db
* Generate reports for download
* Add SonarQube
* Add more and improve test cases
* Add Makefile
* Dockerize

## Developer by ✒️

* **Daniel Buitrago** - Documentation and programming - [jsdnlb](https://github.com/jsdnlb)

---
