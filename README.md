# RestartR

RestartR is an API for collecting observations.
RestartR observations are 
* **JSON**: Observations are JSON objects.
* **Schemaless**. That is, it accepts data observations in any syntactically valid JSON object structure.

Operations are:
* **observation**: Use HTTP post requests to record an observation.
* **query**: Query the system for recorded observations.

## Design

RestrtR consists of
* **API**: The observation API for recording observed events.
* **MongoDB**: A document store database supporting schemaless events.
* **Mongo-Express**: A web based user interface for MongoDB

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
To start the stack (RestartR API, MongoDB, Mongo-Express) synchronously:
```
bin/restartr stack up
```
To start the stack in the background:
```
bin/restartr stack start
```
To run the API standalone, assuming you have a databse elsewhere:
```
bin/restartr api --debug
```
To test the observation API:
```
bin/restartr tests add data/a.json 1
```
To test the query API:
```
bin/restartr tests query data/a.json 1
```
### Deployment
As we move towards deployment, we'll create a Kubernetes Helm chart for the environment.
This will use production environment secrets for the various passwords and API keys involved.

### Secrets
Secrets are passed via environment variables in development and production modes:
![image](https://user-images.githubusercontent.com/306971/83798948-0abf9900-a673-11ea-8eda-7e9d51043dab.png)
Defaults are provided in development but cal all be overriden with Docker ENV variables in Kubernetes.

### API Key
The API requires a key which is set via the X-API-Key HTTP header.
The bin/restartr script contains examples:
![image](https://user-images.githubusercontent.com/306971/83805701-5cb9ec00-a67e-11ea-9f29-b234ed8bf29f.png)

### Execution modes
The API can be run in a number of modes within the docker stack.
1. `bin/restartr api` runs it with python.
2. `bin/restartr api --debug` runs it with python in debug mode.
3. `bin/restartr api_prod` runs it in gunicorn.
All are accessible in the docker container.
![image](https://user-images.githubusercontent.com/306971/83798858-dfd54500-a672-11ea-9176-fd1d862dca72.png)

### Example
Running the query test:
![image](https://user-images.githubusercontent.com/306971/83798235-f62ed100-a671-11ea-8a7b-1e2497c0e3a5.png)
Output when running with the development server:
![image](https://user-images.githubusercontent.com/306971/83798135-c67fc900-a671-11ea-9d0e-510e84ae5114.png)


