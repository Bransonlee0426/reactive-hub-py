#!/bin/bash
# 資料庫操作的便利別名
# 使用方法: source scripts/db_aliases.sh

# 設定專案根目錄
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔧 正在設定資料庫快速指令..."

# 基本資料庫連線
alias dbconn='docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb'
alias dbshell='docker exec -it reactive-hub-py-db-dev bash'

# 快速查詢指令
alias dbtables='docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "\dt"'
alias dbsize='docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT pg_size_pretty(pg_database_size(current_database()));"'
alias dbversion='docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT version();"'

# 資料庫狀態
alias dbstatus='docker ps | grep reactive-hub-py-db-dev'
alias dblogs='docker logs reactive-hub-py-db-dev'

# 使用我們的工具
alias dbquick="$PROJECT_ROOT/scripts/db_quick.sh"
alias dbmgr="cd $PROJECT_ROOT && python db_manager.py"

# SQL 範本
alias sqlhelp="cat $PROJECT_ROOT/scripts/sql_templates.sql | less"

# 開發流程快捷鍵
alias devstart='cd $PROJECT_ROOT && source venv/bin/activate && docker compose up -d'
alias devstop='cd $PROJECT_ROOT && docker compose down'

# 自定義 SQL 查詢函數
dbquery() {
    if [ -z "$1" ]; then
        echo "使用方法: dbquery \"SELECT * FROM table_name;\""
        return 1
    fi
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "$1"
}

# 查看表格結構
dbdesc() {
    if [ -z "$1" ]; then
        echo "使用方法: dbdesc table_name"
        return 1
    fi
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "\d+ $1"
}

# 計算表格記錄數
dbcount() {
    if [ -z "$1" ]; then
        echo "使用方法: dbcount table_name"
        return 1
    fi
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT COUNT(*) FROM $1;"
}

# 查看表格前 N 筆資料
dbsample() {
    local table_name="$1"
    local limit="${2:-10}"
    
    if [ -z "$table_name" ]; then
        echo "使用方法: dbsample table_name [limit]"
        echo "範例: dbsample users 5"
        return 1
    fi
    
    echo "📊 表格 '$table_name' 的前 $limit 筆資料："
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT * FROM $table_name LIMIT $limit;"
}

# 創建示例表格和資料
dbcreate_sample() {
    echo "🛠️  正在創建示例表格 'sample_items'..."
    
    # 創建表格的 SQL
    local create_sql="
    CREATE TABLE IF NOT EXISTS sample_items (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price INTEGER,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );"
    
    # 插入示例資料的 SQL
    local insert_sql="
    INSERT INTO sample_items (name, description, price) VALUES 
    ('iPhone 15', '最新款 iPhone', 30000),
    ('MacBook Pro', '專業筆記型電腦', 60000),
    ('AirPods Pro', '降噪耳機', 8000),
    ('iPad Air', '輕薄平板電腦', 20000),
    ('Apple Watch', '智慧手錶', 12000)
    ON CONFLICT DO NOTHING;"
    
    # 執行 SQL
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "$create_sql"
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "$insert_sql"
    
    echo "✅ 示例表格和資料創建完成！"
    echo "💡 可以使用 'dbsample sample_items' 查看資料"
}

# 資料庫健康檢查
dbhealth() {
    echo "🏥 資料庫健康檢查："
    echo ""
    
    # 檢查容器狀態
    echo "📦 容器狀態："
    docker ps | grep reactive-hub-py-db-dev || echo "❌ 資料庫容器未運行"
    
    echo ""
    echo "🔗 連線測試："
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT 'Database connection OK' as status;" 2>/dev/null || echo "❌ 資料庫連線失敗"
    
    echo ""
    echo "📊 資料庫資訊："
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT version();" 2>/dev/null | head -3
    
    echo ""
    echo "💾 資料庫大小："
    docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "SELECT pg_size_pretty(pg_database_size('myapidb')) as database_size;" 2>/dev/null
}

# 快速資料庫重置（開發用）
dbreset() {
    echo "⚠️  警告：這將刪除所有資料！"
    read -p "確定要重置資料庫嗎？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  正在重置資料庫..."
        docker exec -it reactive-hub-py-db-dev psql -U user -d myapidb -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        echo "✅ 資料庫已重置"
        echo "💡 可以使用 'dbcreate_sample' 創建示例資料"
    else
        echo "❌ 取消重置"
    fi
}

echo "✅ 資料庫快速指令設定完成！"
echo ""
echo "📋 可用的指令："
echo "  🔗 基本操作："
echo "    dbconn          - 連接到資料庫"
echo "    dbtables        - 列出所有表格" 
echo "    dbquery         - 執行 SQL 查詢"
echo "    dbdesc          - 查看表格結構"
echo ""
echo "  📊 資料查看："
echo "    dbcount         - 計算記錄數"
echo "    dbsample        - 查看表格範例資料"
echo "    dbsize          - 查看資料庫大小"
echo "    dbversion       - 查看資料庫版本"
echo ""
echo "  🛠️  開發工具："
echo "    dbhealth        - 資料庫健康檢查"
echo "    dbcreate_sample - 創建示例表格和資料"
echo "    dbreset         - 重置資料庫（謹慎使用）"
echo "    sqlhelp         - 查看 SQL 範本"
echo ""
echo "  🚀 環境管理："
echo "    devstart        - 啟動開發環境"
echo "    devstop         - 停止開發環境"
echo "    dbstatus        - 查看容器狀態"
echo "" 