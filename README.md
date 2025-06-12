# exif-inspect
Offline Exif viewer

## Running

```bash
python app.py
```

## Docker deployment

On Macos, make sure Colima is started

```bash
colima status
colima start -f
```

```bash
docker build --platform=linux/amd64 -t exif-inspect .
docker save -o exif-inspect.tar exif-inspect
scp exif-inspect.tar user@your-vps-ip:/path/on/vps/
```

on VPS:
```bash
docker load -i exif-inspect.tar
docker run -d -p 5050:5000 exif-inspect
```

Inspect container from inside :
```bash
docker exec -it <ID> sh
```