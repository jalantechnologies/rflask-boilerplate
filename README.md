# Boilerplate - FRM

Boilerplate project for Flask, React & MongoDB based projects. This README documents the steps necessary to get your
application up and running.

## Table of Contents

- [Boilerplate - FRM](#boilerplate---frm)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Configuration](#configuration)
  - [Scripts](#scripts)
  - [Deployment](#deployment)

## Getting Started

**Quickstart:**

- This project supports running the application with all the required dependencies using `docker compose`.
- Install [docker](https://docs.docker.com/engine/install/).
- Run `docker compose -f docker-compose.dev.yml up` (Add `--build` to force rebuild when new dependencies have been
  added).
- The application should open up automatically. If it doesn't, go to `http://localhost:3000`.
- Make required changes for development. Both backend and frontend should hot reload, and server restart is not
  required.

**Bonus:**

- On running `serve`, the frontend server is at `http://localhost:3000`.
- On running `serve`, the backend server is at `http://localhost:8080`.
- To connect to MongoDB server using a client, use `mongodb://localhost:27017`.

**Pre Requirements:**

- Python (v3.11)
- Node (v22.13.1) - [Download](https://nodejs.org/download/release/v22.13.1/)
- MongoDB (v5) - [Download](https://www.mongodb.com/docs/manual/installation/)

**Scripts:**

- Install dependencies - `npm install`
- Install Python dependencies - `pipenv install --dev`
- Build Project - `npm run build`
- Start Application (without HotReload) - `npm start`
- Start Application (with HotReload enabled) - `npm run serve`
  - To disable opening up the browser automatically, set `WEBPACK_DEV_DISABLE_OPEN` to `true`.
- Lint Check - `npm run lint`
- Format Code - `npm run fmt`

## Configuration

In the `config` directory:

We are keeping config schema as a environment specific yml files.

In the `config` directory:

- Consult/update `custom-environment-variables.yml` for loading values via environment. This overrides any value set in files defined below.
- Consult/update `development.yml` for values at development. (The default env)
- Consult/update `testing.yml` for values at testing. `APP_ENV` must be set to `testing` for this.
- Consult/update `preview.yml` for values at `preview` `APP_ENV` must be set to `preview` for this.
- Consult/update `production.yml` for values at production. `APP_ENV` must be set to `production` for this.
- Consult/update `default.yml` for **constant values only**. Define entries here which will remain same across deployments.

**INFO:** Based on the environment which will be passed during spawning the server as an argument
 with `APP_ENV=<environment_name>`, this will further load the schema accordingly.

**INFO:** `default.yml` config file lists the all available entries which the system uses. For creating a new config entry: 
- If the config value tends to change across deployments, provide `null` for the same in `default.yml` and value should be provided in respective deployment file.
- If the config value is supposed to be same across deployments, provide the same in `default.yml`.

**INFO:** For injecting environment variables, can add `.env` file in the application root directory.

### Custom Environment Variables

Some deployment situations rely heavily on environment variables to configure secrets and settings best left out of a codebase.

For enabling this we have a dedicated file called `custom-environment-variables.yml` for mapping the environment variable names into our configuration schema.
For example:

```yml  
mongodb:
  uri: "MONGODB_URI" 

inspectlet:  
  key: "INSPECTLET_KEY"  

papertrail:  
  host: "PAPERTRAIL_HOST"  
  port:  
    __name: "PAPERTRAIL_PORT"  
    __format: "number"  
```  
... would cause our Config Manager to check for environment variables `MONGODB_URI` and `INSPECTLET_KEY`. If they exist they would override `mongodb.uri` and `inspectlet.key` in our configuration.

For `PAPERTRAIL_PORT` it will try to parse the found environment variable according to the specified format in `__format` (`number` in this case) and extend the values for `papertrail.port`. Empty environment variables are ignored, and their mappings have no effect on your config.

**Available `__format` types**:  
- `boolean`  
- `number`  

**Precedence**: Custom environment variables override all other configuration files, including `default.yml` and `{app_env}.yml`.  


**UI Config:**

In case of need of config values at client-side, this will make an internal request to the backend server to get the
desired config schema in the form of JSON.

## Scripts

This application also supports running one off scripts. Helpful during development or running cron jobs.

Steps:

- Create a python file under - `src/apps/backend/scripts` (ex - `my-script.py`)
- Run the script using npm - `npm run script --file=example_worker_script`

## Deployment

This project deploys on Kubernetes via GitHub actions using workflows defined
in [GitHub CI](https://github.com/jalantechnologies/github-ci).
