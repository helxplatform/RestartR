# RestartR

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
