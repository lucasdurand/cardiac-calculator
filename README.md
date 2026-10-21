# cardiac-calculator
An MVP for a simple calculator app with cardiac-obstetric applications

## Usage
...

## Development

### Installation

Install [uv](https://docs.astral.sh/uv/), then create the virtual environment with `uv sync` and run the app with `uv run python mvp.py`

### Deployment

The app runs on [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3) standard (F1 instance, scales to zero, within the free tier), as the `cardiac-calculator` service.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install), then `gcloud init` and pick your project
1. If you changed dependencies, regenerate `requirements.txt` (App Engine installs from it): `uv export --no-dev --no-hashes -o requirements.txt`
1. Deploy with `gcloud app deploy`
1. View it with `gcloud app browse -s cardiac-calculator`

Pushes to `main` deploy automatically via [the Deploy workflow](.github/workflows/deploy.yml), which needs a `GCP_SA_KEY` Actions secret (service-account key JSON). It also fails if `requirements.txt` is out of date with `uv.lock`.

App Engine requires a project's first service to be `default`, so in a brand new project remove the `service:` line from `app.yaml` for the first deploy.
