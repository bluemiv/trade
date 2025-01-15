# 자동매매 스크립트

## 무한 매매

local 환경

```
python infinit_trade.py  # 1회
python loop_infinit_trade.py  # 무한루프
```

docker 환경

```bash
docker build -t trade .
docker run --name trade -d trade
```