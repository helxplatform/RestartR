# RestartR

RestartR is an API for collecting study observations.

For now, it is schemaless. That is, it accepts data observations in any format.

## Development

### Installation
```
git clone <repo>
cd <repo>
python3 -m venv ../restartr
source ../restartr/bin/activate
pip install -r requirements.txt
```
### Running
To start the stack (RestartR API, MongoDB, Mongo-Express):
```
bin/restartr stack up
```
To run the API standalone, assuming you have a databse elsewhere:
```
bin/restartr api --debug
```
To test the API:
```
bin/restartr tests data/a.json 1
```

### Deployment
As we move towards deployment, we'll create a Kubernetes Helm chart for the environment.
This will use production environment secrets for the various passwords and API keys involved.

