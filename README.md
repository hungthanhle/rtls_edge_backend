0. Set up
Install Dependency
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Initialize DB
```
python db.py
```
1. Chạy Tag Simulator
```
python tag_simulator.py
```
2. Chạy Server tiếp nhận
```
python main.py
```
3. Chạy API Server (FastAPI)
```
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
