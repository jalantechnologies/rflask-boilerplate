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

In the `config` directory, we maintain environment-specific YAML files to manage application configurations.

### Configuration Files

- **`custom-environment-variables.yml`** – Overrides values using environment variables.
- **`development.yml`** – Configuration for the development environment (default).
- **`testing.yml`** – Configuration for the testing environment (`APP_ENV` must be set to `testing`).
- **`preview.yml`** – Configuration for the preview environment (`APP_ENV` must be set to `preview`).
- **`production.yml`** – Configuration for the production environment (`APP_ENV` must be set to `production`).
- **`default.yml`** – Stores constant values that remain unchanged across deployments.

### Environment Selection
The configuration schema is loaded based on the `APP_ENV` value provided when starting the server:
`APP_ENV=<environment_name>`

### `default.yml` Guidelines
- If a configuration value **varies across deployments**, set it to `null` in `default.yml` and define it in the respective environment-specific file.
- If a configuration value **remains the same across all deployments**, define it directly in `default.yml`.

### `.env` Support
For injecting environment variables, you can add a `.env` file in the application root directory.

## Custom Environment Variables
Some deployment scenarios require environment variables for handling sensitive data or settings that should not be stored in the codebase.

To facilitate this, we use `custom-environment-variables.yml` to map environment variables to configuration keys.

### Example Mapping:
```yml
mongodb:
  uri: "MONGODB_URI"

inspectlet:
  key: "INSPECTLET_KEY"

demo:
  host: "DEMO_HOST"
  port:
    __name: "DEMO_PORT"
    __format: "number"
```

#### Behavior:
- If the environment variable `MONGODB_URI` exists, it will override `mongodb.uri`.
- If `INSPECTLET_KEY` is present, it will override `inspectlet.key`.
- `DEMO_PORT` will be converted to a number before overriding `demo.port`.
- Empty environment variables are ignored and do not affect the configuration.

### Available `__format` Types:
- `boolean`
- `number`

### Configuration Precedence:
1. **Custom Environment Variables** (highest priority)
2. **Environment-Specific Configuration Files** (e.g., `development.yml`, `production.yml`)
3. **`default.yml`** (lowest priority, used as fallback)


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
