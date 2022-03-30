# JIRA Tickets Per Minute

Jira TPM ("Tickets per minutee") is a complete, secure and scalable microservice example written in Python (and compiled to executable C code) to automatically create Jira tickets for testing purposes and provide up to the minute historical reporting over thos tickets with High or Highest severity. 

The service is written in Python and then compiled to C byte code. However this version includes the source files as a fallback. so it can be run without compiling *make build-arch* (or *docker-compose up*).

To keep things simple for this demo, neither Docker nor compilation is required. All that's needed for a fully working instance is to run the following commands:

1. `./install.sh`,
2. `python3 run.py`

This (obviously) assumes you have python3 available in your execution context.


# Table of contents

  * [Overview](#jira-tickets-per-minute)
  * [Build](#build)
  * [Install](#install)
  * [Run](#run)  
  * [Deploy](#deploy)
    * [Docker Compose](#docker-compose)
    * [Docker Factory](#docker-factory)
  * [Security](#security)
    * [Client Access](#token-based-secure-access)
    * [Secrets Management](#vault-secrets-management)
  * [Known Issues](#knownissues)
  * [License](#license)
  * [Contact](#Contact)


### BUILD

Jira TPM is intended to be run from compiled binaries rather than source files. While not required for this demo, building for your platform is supported using the supplied Makefile scripts. This will compile the python files down to C binaries to run directly on your architecture.

```
make build
```

This is an alias for `build-arch` which compiles from the source files (found in `lib/c`) to executable objects in `lib/ext`.

The included Makefile also supports options for `build-source` which creates the C source code used by build-arch, and `build-local` which, intended for developers, skips the intermediate step and directly compiles the binaries for your local architecture.

This demo version includes fallback to the original source files, so you do not need to compile for your architecture to run.

## INSTALL

### Bare Installation

Demo does not presume Docker is present, or Conda, (or Poetry) but does require Pip to be available.

To install all dependencies and run the app, simply exectute the start script in the root directory.

* ``./install.sh``

This will first install the required libaries using

* ``pip install -r requirements.txt``

## RUN

After installing the requirements with pip, a command line demo can be started with:

* ``source .env``
* ``source .auth``
* ``python3 run.py``

This will start an interactive CLI based demo of the service.

Passing run.py the --help flag (or -h) will provide the possible options to pass, which correspond to the steps listed in the take home assignment, namely:  

* --create-tickets (``run.py -c``) creates ~100 random Jira tickets over the course of an hour.
* --fetch-tickets (``run.py -f``) retrieves all High and Highest severity tickets from Jira and saves to Postgres backend.
* --plot-data (``run.py -p``) launches a visual dashboard displaying tickets per minute on port 8050.

The run script also support options for creating and dropping the tickets table in the backend database, as long as the Postgres host, user and credentials are supplied in the included .env and .auth files.

* create-table (``run.py -t``) creates tickets table in Postgres backend.
* drop-table (``run.py -t``) drops tickets table in Postgres backend.


## DEPLOY

The application aims to provide 2 implementations for containerized deployments using either Docker compose to bring up all service containers running locally or a custom “Docker factory” that will build a complete Docker image from the supplied Dockerfile, and deploy it to a remote cloud server using credentials sourced from your environment settings, and automatically run it. This is pre-configured for AWS but can be easily adapted for any Posix compatible endpoint. Not included here is an option to deploy with Terraform or CloudFormation.

### Docker Compose

Standard Docker deployment builds and runs 3 containers:
* App-server
* Database-server
* Front-end

All 3 containers can be run on a single server, or deployed to different endpoints.

### Docker Factory

The supplied Docker factory automatically creates a completely build Docker image, copies it to a remote server and starts it up on the specified port. This requires credentials for a running cloud server such as EC2. Integrations are not currently provided for Fargate.


## Security

### Token Based Secure Access

In order to make included functionality available through an API, considerations are included for requiring for clients to provide autherization credentials use the API n the fom of a secure token (JWT). This version of app (v0.0.1) does not implement the secure API for reasons of time.

### Secured with Vault

With client side access secured by access tokens, the backend is to be protected by Hashicorp Vault. In order to securely access the database credentials are sourced from a Vault server running on AWS and set with a TTL of one hour.

The secrets management service can be turned on/off; the demo is configured without Vault (mainly for reasons of time) with ``USE_VAULT = False`` in ``config/postgres.py``.


## KNOWN ISSUES

### Wekzeug
  * The python 3.9 version of werkzug 2.0.1, required by flask >= 2.0.1 is known to be problematic on some systems. If such issue is encountered, a less than optimal workaround is to use the Python 3.7 version of Werkzeug 2.0.1, rather than the Python 3.9 version of this library.

### Average tickets per minute  
  * This application creates tickets with an average of 1.5 TPM (tickts per minute) but to be precise about the requirements (~100 tickets an hour) that should be 1.66 tpm. This is because we use an integer to randomly generate the number of tickets rather than a float. However, since we are only displaying the High and Highest priority tickets, the resulting graph can be somewhat sparse, so this could also be increased to 2.2 TPM (by setting MAX_PER_MIN to 5) so we have a better dataset for visualization.

### Bar chart vs. Histogram
  * The stated requirements are to display hourly ticket data as a bar chart, however for data of this shape a histogram is more commonly used. Histograms visualize quantitative data or numerical data, whereas bar charts display categorical variables. Given a bit more time would like to make this selectable in the front end app.

### Severity vs. Priority
  * The semantics around ticket priority vs issue severity can sometimes be ambivalent. In general, incidents have severity (eg. Blocker, Critical, Major, Minor) and tickets have priority (which are intended to be ordinal.) Thus Jira uses "priority" rather than 'severity' and provides the default values of Lowest, Low, Medium, High and Highest, to which you may add any custome priority levels you like. Given more time would have liked to implement this part of the API as well.

### Hour handling   
  * As the requirements specify creating one hours worth of tickets, the current implementation doesn't include handlers for selecting *which* hour to display, or handling for any tickets falling outside of the hour. Given more time this is obviously something that would greatly enhance functionality.

### Sample Data
  * A psql dump of sample data is included in (in /data/ directory) however no functionality is included for automatically loading it. (`psql -h <hostname> -U <username> -f data/jira_tpm_demo.psql`)

## ⚖ LICENSE

All original code here with is copyright 2021 Forest Mars / Continuum Software. Provided to Silk Security for purposes of demonstration.

## CONTACT

[via email](mailto:themarsgroup@gmail.com)
