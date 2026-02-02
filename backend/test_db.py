"""Quick test script to verify database setup"""
import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="agrogradeai",
        user="postgres",
        password="Deep@123"
    )
    cur = conn.cursor()
    
    # Check tables
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    tables = [r[0] for r in cur.fetchall()]
    
    print("=" * 50)
    print("DATABASE CONNECTION: SUCCESS")
    print("=" * 50)
    print(f"Database: agrogradeai")
    print(f"Tables found: {len(tables)}")
    
    if tables:
        print("\nTables:")
        for t in tables:
            print(f"  - {t}")
    else:
        print("\n[!] No tables found - schema not applied yet!")
        print("    Run: psql -U postgres -d agrogradeai -f database/schema.sql")
    
    conn.close()
    print("\n" + "=" * 50)
    
except Exception as e:
    print(f"DATABASE CONNECTION FAILED: {e}")
