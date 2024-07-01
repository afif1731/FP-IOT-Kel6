# How to Run Bcakend

### Create Python Environment (Recommended for Development)
```
py -3.9 -m venv .
```

### Activate Virtual environment (Windows)
```
./Scripts/activate
```

### Install Requirements
```
pip install -r requirements.txt
```

### Run Docker for Database
```
docker compose up -d
```

### Migrate Database
```
prisma migrate dev --schema ./prisma/schema.prisma
```

### Use Data Seeder
```
python .\seeder.py
```

### Run Server
```
python .\main.py
```
