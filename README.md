# Reactive Hub Python 專案

## 🚀 開發流程快速指南

### 每次開發開始時執行：
```bash
# 1. 啟動虛擬環境
source venv/bin/activate

# 2. 啟動資料庫（背景執行）
docker compose up -d

# 3. 驗證環境（可選）
docker ps                    # 確認資料庫容器運行
python --version            # 確認 Python 環境
```

### 每次開發結束時執行：
```bash
# 1. 停止資料庫
docker compose down

# 2. 取消虛擬環境
deactivate
```

## Python 虛擬環境設定

### 建立虛擬環境
```bash
python3 -m venv venv
```

### 啟動虛擬環境
```bash
source venv/bin/activate
```

### 取消虛擬環境
```bash
deactivate
```

### 驗證虛擬環境
啟動虛擬環境後，您應該會看到：
- 終端機提示符前會出現 `(venv)` 標示
- 現在可以直接使用 `python` 命令（而不需要 `python3`）

```bash
# 檢查 Python 路徑
which python

# 檢查 Python 版本
python --version
```

## 套件安裝

### 安裝專案相依套件
```bash
pip install -r requirements.txt
```

### 主要套件說明
- **FastAPI**: 現代、快速的 Python Web 框架
- **Uvicorn**: ASGI 服務器，用於運行 FastAPI 應用程式
- **SQLAlchemy**: Python SQL 工具包和物件關聯映射 (ORM)
- **psycopg2-binary**: PostgreSQL 資料庫適配器

## 資料庫設定 (Docker)

### 前置需求：安裝 Docker Desktop
1. 前往 [Docker Desktop 官方網站](https://www.docker.com/products/docker-desktop/)
2. 下載適用於 macOS 的 Docker Desktop
3. 安裝並啟動 Docker Desktop
4. 確認 Docker 已正常運行：
   ```bash
   docker --version
   docker compose version
   ```

### 啟動 PostgreSQL 資料庫
```bash
docker compose up -d
```

### 驗證資料庫運行狀態
```bash
docker ps
```
您應該看到一個 `postgres:15` 容器正在運行。

### 停止資料庫
```bash
docker compose down
```

### 資料庫連線資訊
- **主機**: localhost
- **連接埠**: 5432
- **資料庫名稱**: myapidb
- **使用者名稱**: user
- **密碼**: password

### 連線字串範例
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/myapidb"
```

## 專案說明
這是一個使用 FastAPI 框架的 Python Web 應用程式專案，整合了 SQLAlchemy ORM 和 PostgreSQL 資料庫。使用 Docker Compose 來管理開發環境中的資料庫服務。

## 注意事項
- 請確保在專案開發時先啟動虛擬環境
- 安裝新套件時請在虛擬環境中進行
- 完成開發後記得取消虛擬環境
- 所有相依套件已列在 `requirements.txt` 中 