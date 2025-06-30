-- 🗂️ SQL 查詢範本檔案
-- 常用的 SQL 查詢，可以複製使用

-- ==================== 資料庫探索 ====================

-- 列出所有表格
\dt

-- 列出所有表格（包含詳細資訊）
\dt+

-- 列出所有 schema
\dn

-- 查看特定表格結構
\d+ table_name

-- ==================== 表格資訊查詢 ====================

-- 查看所有表格及其記錄數
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals
FROM pg_stats 
WHERE schemaname = 'public';

-- 查看表格大小
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- ==================== 常用資料查詢 ====================

-- 取得表格基本統計
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT id) as unique_ids
FROM table_name;

-- 查看最近建立的記錄
SELECT * FROM table_name 
ORDER BY created_at DESC 
LIMIT 10;

-- 查看啟用的記錄
SELECT * FROM table_name 
WHERE is_active = true 
LIMIT 10;

-- ==================== 資料操作範本 ====================

-- 插入新記錄
INSERT INTO table_name (name, description, is_active) 
VALUES ('範例名稱', '範例描述', true);

-- 更新記錄
UPDATE table_name 
SET description = '新的描述', updated_at = NOW() 
WHERE id = 1;

-- 軟刪除（設定 is_active = false）
UPDATE table_name 
SET is_active = false, updated_at = NOW() 
WHERE id = 1;

-- ==================== 除錯和分析 ====================

-- 查看正在執行的查詢
SELECT pid, now() - pg_stat_activity.query_start AS duration, query 
FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- 查看連線數
SELECT COUNT(*) FROM pg_stat_activity;

-- 查看資料庫版本
SELECT version();

-- ==================== 開發用查詢 ====================

-- 查看某欄位的唯一值
SELECT DISTINCT column_name FROM table_name ORDER BY column_name;

-- 計算某欄位的分布
SELECT column_name, COUNT(*) as count 
FROM table_name 
GROUP BY column_name 
ORDER BY count DESC;

-- 查找空值
SELECT COUNT(*) as null_count 
FROM table_name 
WHERE column_name IS NULL;

-- ==================== 資料庫維護 ====================

-- 查看索引使用情況
SELECT 
    t.tablename,
    indexname,
    c.reltuples AS num_rows,
    pg_size_pretty(pg_relation_size(quote_ident(t.tablename)::text)) AS table_size,
    pg_size_pretty(pg_relation_size(quote_ident(indexrelname)::text)) AS index_size
FROM pg_tables t
LEFT OUTER JOIN pg_class c ON c.relname=t.tablename
LEFT OUTER JOIN (
    SELECT c.relname AS ctablename, ipg.relname AS indexname, x.indnatts AS number_of_columns, idx_scan, idx_tup_read, idx_tup_fetch, indexrelname, indisunique FROM pg_index x
    JOIN pg_class c ON c.oid = x.indrelid
    JOIN pg_class ipg ON ipg.oid = x.indexrelid
    JOIN pg_stat_all_indexes psai ON x.indexrelid = psai.indexrelid
) AS foo
ON t.tablename = foo.ctablename
WHERE t.schemaname='public'
ORDER BY 1,2; 