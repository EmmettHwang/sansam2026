"""
데이터베이스 테이블 자동 생성 스크립트
"""

import mysql.connector
from mysql.connector import Error

# DB 설정
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'Dodan1004!',
    'database': 'sansam'
}

def create_tables():
    """데이터베이스 테이블 생성"""
    print("\n" + "="*60)
    print("🔧 데이터베이스 생성 및 테이블 생성")
    print("="*60)
    
    try:
        # DB 연결 (데이터베이스 미지정)
        print(f"\n📡 DB 연결 중: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        db_config_no_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
        connection = mysql.connector.connect(**db_config_no_db)
        cursor = connection.cursor()
        
        print("✅ DB 연결 성공!")
        
        # 데이터베이스 생성
        print("\n📋 'sansam' 데이터베이스 생성 중...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ '{DB_CONFIG['database']}' 데이터베이스 생성 완료")
        
        # 데이터베이스 선택
        cursor.execute(f"USE {DB_CONFIG['database']}")
        print(f"✅ '{DB_CONFIG['database']}' 데이터베이스 선택 완료")
        
        # 1. gallery_images 테이블 생성
        print("\n📋 gallery_images 테이블 생성 중...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gallery_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                original_name VARCHAR(255),
                file_path VARCHAR(500) NOT NULL,
                file_size INT,
                width INT,
                height INT,
                is_representative TINYINT(1) DEFAULT 0,
                display_order INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_representative (is_representative)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ gallery_images 테이블 생성 완료")
        
        # 2. products 테이블 생성
        print("\n📋 products 테이블 생성 중...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                image_path VARCHAR(500),
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ products 테이블 생성 완료")
        
        # 3. orders 테이블 생성
        print("\n📋 orders 테이블 생성 중...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                customer_name VARCHAR(100) NOT NULL,
                customer_phone VARCHAR(20) NOT NULL,
                customer_email VARCHAR(255),
                delivery_address TEXT NOT NULL,
                delivery_message TEXT,
                total_amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_order_number (order_number),
                INDEX idx_status (status),
                FOREIGN KEY (product_id) REFERENCES products(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ orders 테이블 생성 완료")
        
        connection.commit()
        
        # 테이블 목록 확인
        print("\n📊 생성된 테이블 확인:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("🎉 모든 테이블 생성 완료!")
        print("="*60)
        print("\n👉 이제 관리자 페이지를 새로고침하세요!")
        print("   http://localhost:8000/admin")
        print("="*60 + "\n")
        
        return True
        
    except Error as e:
        print(f"\n❌ 에러 발생: {e}")
        return False

if __name__ == "__main__":
    create_tables()
