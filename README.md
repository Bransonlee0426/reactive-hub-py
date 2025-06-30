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

# 4. 載入資料庫工具（可選）
source scripts/db_aliases.sh  # 載入資料庫快速指令
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

## 🗄️ 資料庫管理工具

專案提供了一套完整的資料庫管理工具，讓您可以通過簡單的命令列指令進行所有資料庫操作。

### 啟動資料庫工具
```bash
# 載入所有資料庫快速指令
source scripts/db_aliases.sh
```

### 🔗 基本操作
```bash
dbconn          # 連接到資料庫
dbtables        # 列出所有表格
dbquery "SQL"   # 執行 SQL 查詢
dbdesc table    # 查看表格結構
```

### 📊 資料查看
```bash
dbcount users        # 計算記錄數
dbsample users 5     # 查看前5筆資料
dbsize              # 查看資料庫大小
dbversion           # 查看資料庫版本
```

### 🛠️ 開發工具
```bash
dbhealth           # 資料庫健康檢查
dbcreate_sample    # 創建示例表格和資料
dbreset           # 重置資料庫（謹慎使用）
sqlhelp           # 查看 SQL 範本
```

### 🚀 環境管理
```bash
devstart          # 啟動開發環境
devstop           # 停止開發環境
dbstatus          # 查看容器狀態
```

### 使用範例
```bash
# 1. 載入工具
source scripts/db_aliases.sh

# 2. 創建示例資料
dbcreate_sample

# 3. 查看資料
dbtables
dbsample sample_items 3

# 4. 執行查詢
dbquery "SELECT COUNT(*) FROM sample_items WHERE price > 10000;"
```

### SQL 範本參考
專案還提供了 `scripts/sql_templates.sql` 檔案，包含常用的 SQL 查詢範本，可以使用 `sqlhelp` 命令查看。

## 專案說明
這是一個使用 FastAPI 框架的 Python Web 應用程式專案，整合了 SQLAlchemy ORM 和 PostgreSQL 資料庫。使用 Docker Compose 來管理開發環境中的資料庫服務。

## 注意事項
- 請確保在專案開發時先啟動虛擬環境
- 安裝新套件時請在虛擬環境中進行
- 完成開發後記得取消虛擬環境
- 所有相依套件已列在 `requirements.txt` 中 