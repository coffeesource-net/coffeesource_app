# Coffeesource.net

[Coffeesource.net](Coffeesource.net) is an open source project built using Python for develop tools using the Steem blockchain.

## Architecture

The application has been developed using [Django](https://www.djangoproject.com/) and [steem-python](https://github.com/steemit/steem-python) for access to the Steem blockchain. For run the application locally, a [Docker](https://www.docker.com/) image has been configured on the project.

## Run the project

For run the project in a local enviroment, follow next steps:

1. **Install Docker**.

Download Docker from his [offical website](https://docs.docker.com/engine/installation/) and install it.

2. **Clone the project**.

Clone the project code locally using [Git](https://git-scm.com/):

    git clone https://github.com/coffeesource-net/coffeesource_app.git

3. **Build the Docker image**

Make sure that Docker is running. Move to the root project folder and run the following command:

    docker-compose build

4. **Run the project**

Run the following command for run the project:

    docker-compose up

Now you can visit the coffeesource.net site locally navigating to *localhost:8000* in your browser.
