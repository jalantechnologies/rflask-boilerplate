# Boilerplate - FRM


Boilerplate project for Flask, React & MongoDB based projects. This README documents whatever steps are necessary to get your application up and running.

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Deployment](#deployment)


## Getting Started

**Quickstart:**

- This project supports running the application with all the required dependencies using `docker compose`
- Install [docker](https://docs.docker.com/engine/install/)
- Run `docker compose -f docker-compose.dev.yml up` (Add `--build` to force rebuild when new dependencies have been added)
- Application should open up automatically. In case it doesn't, go to - `http://localhost:3000`
- Make required changes for development. Both backend and frontend should hot reload and server restart is not required.

**Bonus:**

- On running `serve`, frontend server is at - `http://localhost:3000`
- On running `serve`, backend server is at - `http://localhost:8080`
- To connect to MongoDb server using a client, can use - `mongodb://localhost:27017`

**Pre Requirements:**
- Python (v3.11)
- Node (v14.17) - [Download](https://nodejs.org/en/download/)
- MongoDb (v5) - [Download](https://www.mongodb.com/docs/manual/installation/)

**Scripts:**

- Install dependencies - `npm install`
- Build Project - `npm build`
- Start Application (without HotReload) - `npm start`
- Start Application (with HotReload enabled) - `npm run serve`
  - To disable opening up browser automatically, set `WEBPACK_DEV_DISABLE_OPEN` to `true`.
- Run Lint (JavaScript and TypeScript) - `npm run lint:ts`
- Run Lint (Python and MyPy) - `npm run lint:py`
- Run Lint (Markdown) - `npm run lint:md`

## Configuration

In the `src/apps/backend/settings/` directory:

We are keeping config as an schema environment specific

Example -
- For development - we have `development.py` and so for other environment

Based on environment which will be passed during spawning the server as an argument with `APP_ENV=<environment_name>`, this will further load the schema accordingly

Note -
- `default.py`, This file will be using to keep all our **constant value**
- If no enviroment name is passed the default environment would be considered as `development`

**UI Config:**
In case of need of config values at client side, this will make internal request to backend server to get the desired config schema in the form of json

## Deployment

This project deploys on Kubernetes via GitHub actions using workflows defined in [GitHub CI](https://github.com/jalantechnologies/github-ci).

**Version:**

This project uses [v1](https://github.com/jalantechnologies/github-ci/tree/v1)

**Features:**

- Deployment on Digital Ocean kubernetes cluster
- Inbuilt docker registry integration
- Production rollout on `main` branch update
- Preview environment on Pull Requests
- Configuration management via Doppler
- Automatic deployment reload on configuration update


**Setup:**

- Docker registry:
  - This setup supports provisioning our own private self-hosted docker registry
  - This is where the workflow will push the built images and pulled by Kubernetes for deployment
  - Choose a URL which can be used by the registry, example: `registry.example.com`

- Replace / add the values for following in workflow files (can be found in `.github/workflows`):
  - `app_name` - Application name, only allowed `A-Za-z0-9\-`, example: `demo-app`
  - `app_hostname` - Application hostname, example: `demo.example.com`
  - `app_env` - Application environment, example: `production` / `preview`
  - `docker_registry` - Hostname which will be mapped to internal docker registry. Provide here value with chosen docker registry URL in following format - `docker_registry/app_name`.
    For example - `registry.example.com/demo-app`

- Account on Digital Ocean:
  - We will be needing API access token in order to interact with the resources on Digital Ocean
  - Learn about to create a personal access token [here](https://docs.digitalocean.com/reference/api/create-personal-access-token/). Token needs to have both `read` and `write` scope.
  - Take a note of the created **API token**. We will be needing this for rest of the setup.

- Setting up Doppler
  - For configuration management and securely providing access to the secrets to application, this setup uses [Doppler](https://www.doppler.com/) which is allows us to inject configuration parameters as environment variables to application runtime.
  - As mentioned, this is an optional requirement and is meant only for application which require runtime configuration.
  - Application environment will be obtained from value provided for `app_env`. An environment and service token is required per `app_env`.
  - Learn about creating a doppler project and environments [here](https://docs.doppler.com/docs/create-project)
  - Learn about creating a service token in order to access secret associated with an environment [here](https://docs.doppler.com/docs/service-tokens#dashboard-create-service-token)
  - Take a note of the **project**, **environment**, and **service token**. We will be needing this for rest of the setup.
  - This project has support for automatically reloading dependent applications once any configuration updates happens.
    Simply update the desired value in an environment and hit save. Application would reload automatically and will use the updated configurations.

- Setting up SonarQube :: Not supported at the moment

- Install [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

- Create `terraform.tfvars` under `terraform` directory add following content:

```terraform
cluster_issuer_email = "developer@jalantechnologies.com"
do_token             = "<digital ocean token>"
do_cluster_name      = "<cluster name>"
do_alert_email       = "developer@jalantechnologies.com"
docker_registry_host = "<docker registry url>"
```

- Run:
  - `terraform -chdir=terraform init`
  - `terraform -chdir=terraform apply`
  - Wait for process to complete
  - After process has been completed, note down the output which will be presented in form of `key=value` pairs. These will
    be required in subsequent steps.

- Map DNS entries:
  - Map `A` record for value of `docker_registry_host` to value of `ingress_nginx_service_external_ip`
  - Map `A` records for `app_hostname` provided to the workflows to value of `ingress_nginx_service_external_ip`

- Add GitHub secrets to the repository:
  - `DOCKER_USERNAME` - Value of `docker_registry_auth_user`
  - `DOCKER_PASSWORD` - By obtaining value of `docker_registry_auth_password` via - `terraform -chdir=terraform output docker_registry_auth_password`
  - `DOPPLER_PREVIEW_TOKEN` - Doppler token for `preview` environment. See `Setting up Doppler`.
  - `DOPPLER_PRODUCTION_TOKEN` - Doppler token for `production` environment. See `Setting up Doppler`.
  - `DO_ACCESS_TOKEN` - Digital Ocean access token. See `Account on Digital Ocean`.
  - `DO_CLUSTER_ID` - Value of `do_cluster_id`
