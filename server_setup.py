"""
팜랜드 산양산삼 서버 설정 통합 스크립트
- FTP 폴더 생성/확인
- DB 테이블 생성/확인
- 이미지 데이터 관리
"""

import mysql.connector
from mysql.connector import Error
import ftplib
import sys

# ============================================
# 설정
# ============================================
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'Dodan1004!',
    'database': 'sansam'
}

FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/homes/ha/sansam/'
}

CATEGORIES = {
    'farm': '🏞️ 재배지',
    'ginseng': '🌿 산양산삼',
    'process': '⚙️ 선별과정',
    'package': '📦 포장',
    'license': '📄 인허가',
    'live': '📹 Live'
}

# ============================================
# 메인 메뉴
# ============================================
def main_menu():
    """메인 메뉴 표시"""
    while True:
        print("\n" + "="*60)
        print("🏔️  팜랜드 산양산삼 서버 설정")
        print("="*60)
        print("\n📋 메뉴:")
        print("  1. 🚀 전체 초기 설정 (FTP + DB 테이블 생성)")
        print("  2. 📁 FTP 폴더 생성")
        print("  3. 📂 FTP 파일 목록 확인")
        print("  4. 💾 DB 테이블 생성")
        print("  5. 📊 DB 이미지 목록 확인")
        print("  6. 🧹 DB 이미지 데이터 삭제")
        print("  7. 🔍 전체 상태 확인 (FTP + DB)")
        print("  0. 🚪 종료")
        print("="*60)
        
        choice = input("\n선택 (0-7): ").strip()
        
        if choice == '1':
            initial_setup()
        elif choice == '2':
            create_ftp_folders()
        elif choice == '3':
            check_ftp_files()
        elif choice == '4':
            create_db_tables()
        elif choice == '5':
            check_db_images()
        elif choice == '6':
            clean_db_images()
        elif choice == '7':
            check_all_status()
        elif choice == '0':
            print("\n👋 종료합니다.")
            sys.exit(0)
        else:
            print("\n❌ 잘못된 선택입니다!")
        
        input("\n⏸️  계속하려면 Enter를 누르세요...")

# ============================================
# 1. 전체 초기 설정
# ============================================
def initial_setup():
    """FTP + DB 전체 초기 설정"""
    print("\n" + "="*60)
    print("🚀 전체 초기 설정")
    print("="*60)
    
    print("\n📁 1단계: FTP 폴더 생성...")
    if not create_ftp_folders():
        print("\n❌ FTP 폴더 생성 실패!")
        return False
    
    print("\n💾 2단계: DB 테이블 생성...")
    if not create_db_tables():
        print("\n❌ DB 테이블 생성 실패!")
        return False
    
    print("\n" + "="*60)
    print("🎉 전체 초기 설정 완료!")
    print("="*60)
    print("\n👉 이제 관리자 페이지에서 이미지를 업로드하세요!")
    print("   http://localhost:8000/admin")
    print("="*60)
    
    return True

# ============================================
# 2. FTP 폴더 생성
# ============================================
def create_ftp_folders():
    """FTP에 /homes/ha/sansam 폴더 구조 생성"""
    print("\n" + "="*60)
    print("📁 FTP 폴더 생성")
    print("="*60)
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 연결 중: {FTP_CONFIG['host']}:{FTP_CONFIG['port']}")
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        ftp.set_pasv(True)
        
        print("✅ FTP 연결 성공!")
        
        # 베이스 폴더 생성
        base_paths = ['/homes', '/homes/ha', '/homes/ha/sansam']
        
        print("\n📁 베이스 폴더 생성 중...")
        for path in base_paths:
            try:
                ftp.cwd(path)
                print(f"  ✅ {path} 이미 존재")
            except:
                try:
                    ftp.mkd(path)
                    ftp.cwd(path)
                    print(f"  ✅ {path} 생성 완료")
                except Exception as e:
                    print(f"  ❌ {path} 생성 실패: {e}")
                    ftp.quit()
                    return False
        
        # 카테고리 폴더 생성
        print("\n📂 카테고리 폴더 생성 중...")
        for category, name in CATEGORIES.items():
            path = f'/homes/ha/sansam/{category}'
            try:
                ftp.cwd(path)
                print(f"  ✅ {path} 이미 존재 ({name})")
            except:
                try:
                    ftp.mkd(path)
                    print(f"  ✅ {path} 생성 완료 ({name})")
                except Exception as e:
                    print(f"  ⚠️  {path} 생성 실패: {e}")
        
        # 최종 확인
        print("\n📊 최종 폴더 구조:")
        print("  /homes/ha/sansam/")
        for category, name in CATEGORIES.items():
            path = f'/homes/ha/sansam/{category}'
            try:
                ftp.cwd(path)
                print(f"    ├── {category}/ ({name}) ✅")
            except:
                print(f"    ├── {category}/ ({name}) ❌")
        
        ftp.quit()
        
        print("\n🎉 FTP 폴더 생성 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ FTP 에러: {e}")
        return False

# ============================================
# 3. FTP 파일 목록 확인
# ============================================
def check_ftp_files():
    """FTP 파일 목록 확인"""
    print("\n" + "="*60)
    print("📂 FTP 파일 목록 확인")
    print("="*60)
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 연결 중: {FTP_CONFIG['host']}:{FTP_CONFIG['port']}")
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        ftp.set_pasv(True)
        
        print("✅ FTP 연결 성공!")
        
        # /homes/ha/sansam 폴더 확인
        target_path = '/homes/ha/sansam'
        
        try:
            ftp.cwd(target_path)
            print(f"\n✅ {target_path} 폴더 존재!")
        except:
            print(f"\n❌ {target_path} 폴더 없음!")
            print("   👉 '2. FTP 폴더 생성'을 먼저 실행하세요.")
            ftp.quit()
            return False
        
        # 폴더 내용 확인
        print(f"\n📁 {target_path} 폴더 내용:")
        try:
            folders = []
            ftp.retrlines('LIST', folders.append)
            if folders:
                for folder in folders:
                    print(f"  {folder}")
            else:
                print("  (비어있음)")
        except UnicodeDecodeError:
            print("  ⚠️  파일명 인코딩 문제")
        
        # 각 카테고리별 파일 확인
        print("\n📂 카테고리별 파일:")
        for category, name in CATEGORIES.items():
            path = f'{target_path}/{category}'
            try:
                ftp.cwd(path)
                files = []
                ftp.retrlines('LIST', files.append)
                if files:
                    print(f"\n  {name} ({category}): {len(files)}개")
                    for file in files[:3]:  # 최대 3개만 표시
                        print(f"    - {file}")
                    if len(files) > 3:
                        print(f"    ... 외 {len(files) - 3}개")
                else:
                    print(f"\n  {name} ({category}): (비어있음)")
            except:
                print(f"\n  {name} ({category}): ❌ 폴더 없음")
        
        ftp.quit()
        
        print("\n🎉 FTP 확인 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ FTP 에러: {e}")
        return False

# ============================================
# 4. DB 테이블 생성
# ============================================
def create_db_tables():
    """DB 테이블 생성"""
    print("\n" + "="*60)
    print("💾 DB 테이블 생성")
    print("="*60)
    
    try:
        # DB 연결
        print(f"\n📡 DB 연결 중: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ DB 연결 성공!")
        
        # 1. gallery_images 테이블
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
        
        # 2. products 테이블
        print("\n📋 products 테이블 생성 중...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price INT NOT NULL COMMENT '가격 (원)',
                image_path VARCHAR(500) NOT NULL,
                stock INT DEFAULT 999 COMMENT '재고',
                display_order INT DEFAULT 0 COMMENT '표시 순서',
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_active (is_active),
                INDEX idx_order (display_order)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ products 테이블 생성 완료")
        
        # 3. orders 테이블
        print("\n📋 orders 테이블 생성 중...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(200) NOT NULL,
                product_price INT NOT NULL,
                quantity INT NOT NULL,
                total_price INT NOT NULL,
                customer_name VARCHAR(100) NOT NULL,
                customer_phone VARCHAR(20) NOT NULL,
                customer_email VARCHAR(255),
                delivery_address TEXT NOT NULL,
                delivery_message TEXT,
                payment_status VARCHAR(20) DEFAULT 'pending',
                order_status VARCHAR(20) DEFAULT 'ordered',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_order_number (order_number),
                INDEX idx_status (payment_status),
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ orders 테이블 생성 완료")
        
        connection.commit()
        
        # 테이블 목록 확인
        print("\n📊 생성된 테이블:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 DB 테이블 생성 완료!")
        return True
        
    except Error as e:
        print(f"\n❌ DB 에러: {e}")
        return False

# ============================================
# 5. DB 이미지 목록 확인
# ============================================
def check_db_images():
    """DB 이미지 목록 확인"""
    print("\n" + "="*60)
    print("📊 DB 이미지 목록 확인")
    print("="*60)
    
    try:
        # DB 연결
        print(f"\n📡 DB 연결 중: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        print("✅ DB 연결 성공!")
        
        # 카테고리별 이미지 개수
        print("\n📊 카테고리별 이미지 개수:")
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM gallery_images 
            GROUP BY category
        """)
        categories = cursor.fetchall()
        
        total = 0
        if categories:
            for cat in categories:
                name = CATEGORIES.get(cat['category'], cat['category'])
                print(f"  {name}: {cat['count']}개")
                total += cat['count']
            print(f"\n  총 {total}개 이미지")
        else:
            print("  (이미지 없음)")
        
        # 전체 이미지 목록
        if total > 0:
            print("\n📋 최근 업로드 이미지 (최대 10개):")
            cursor.execute("""
                SELECT id, category, filename, original_name, file_size, created_at
                FROM gallery_images
                ORDER BY created_at DESC
                LIMIT 10
            """)
            images = cursor.fetchall()
            
            for img in images:
                name = CATEGORIES.get(img['category'], img['category'])
                size_mb = img['file_size'] / 1024 / 1024
                print(f"\n  [{img['id']}] {name}")
                print(f"      {img['original_name']}")
                print(f"      → {img['filename']} ({size_mb:.2f}MB)")
                print(f"      → {img['created_at']}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 DB 확인 완료!")
        return True
        
    except Error as e:
        print(f"\n❌ DB 에러: {e}")
        return False

# ============================================
# 6. DB 이미지 데이터 삭제
# ============================================
def clean_db_images():
    """DB 이미지 데이터 삭제"""
    print("\n" + "="*60)
    print("🧹 DB 이미지 데이터 삭제")
    print("="*60)
    
    try:
        # DB 연결
        print(f"\n📡 DB 연결 중: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        print("✅ DB 연결 성공!")
        
        # 현재 이미지 개수 확인
        cursor.execute("SELECT COUNT(*) as count FROM gallery_images")
        count = cursor.fetchone()['count']
        
        if count == 0:
            print("\n✅ DB에 이미지 데이터가 없습니다!")
            cursor.close()
            connection.close()
            return True
        
        print(f"\n📊 현재 DB에 {count}개 이미지 데이터가 있습니다.")
        print("\n⚠️  주의: 이 작업은 되돌릴 수 없습니다!")
        
        # 확인
        confirm = input("\n❓ 정말 삭제하시겠습니까? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("\n❌ 취소되었습니다.")
            cursor.close()
            connection.close()
            return False
        
        # 삭제 실행
        print("\n🗑️  이미지 데이터 삭제 중...")
        cursor.execute("DELETE FROM gallery_images")
        connection.commit()
        
        print(f"✅ {count}개 이미지 데이터 삭제 완료!")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 DB 정리 완료!")
        print("👉 이제 이미지를 다시 업로드하세요!")
        
        return True
        
    except Error as e:
        print(f"\n❌ DB 에러: {e}")
        return False

# ============================================
# 7. 전체 상태 확인
# ============================================
def check_all_status():
    """FTP + DB 전체 상태 확인"""
    print("\n" + "="*60)
    print("🔍 전체 상태 확인")
    print("="*60)
    
    # FTP 확인
    print("\n📁 FTP 상태:")
    ftp_ok = check_ftp_connection()
    
    # DB 확인
    print("\n💾 DB 상태:")
    db_ok = check_db_connection()
    
    # 이미지 개수 비교
    if ftp_ok and db_ok:
        print("\n📊 데이터 동기화 상태:")
        compare_ftp_db_counts()
    
    print("\n" + "="*60)
    if ftp_ok and db_ok:
        print("✅ 모든 시스템 정상!")
    else:
        print("⚠️  일부 시스템에 문제가 있습니다.")
    print("="*60)

def check_ftp_connection():
    """FTP 연결 확인"""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        
        # /homes/ha/sansam 폴더 확인
        ftp.cwd('/homes/ha/sansam')
        
        # 카테고리 폴더 개수 확인
        folders = []
        ftp.retrlines('NLST', folders.append)
        
        print(f"  ✅ FTP 연결 성공")
        print(f"  ✅ /homes/ha/sansam 폴더 존재")
        print(f"  ✅ 카테고리 폴더: {len(folders)}개")
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"  ❌ FTP 연결 실패: {e}")
        return False

def check_db_connection():
    """DB 연결 확인"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 테이블 확인
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        required_tables = ['gallery_images', 'products', 'orders']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"  ⚠️  DB 연결 성공")
            print(f"  ❌ 누락된 테이블: {', '.join(missing_tables)}")
            cursor.close()
            connection.close()
            return False
        
        # 이미지 개수 확인
        cursor.execute("SELECT COUNT(*) FROM gallery_images")
        image_count = cursor.fetchone()[0]
        
        print(f"  ✅ DB 연결 성공")
        print(f"  ✅ 필수 테이블 모두 존재")
        print(f"  ✅ 이미지 데이터: {image_count}개")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"  ❌ DB 연결 실패: {e}")
        return False

def compare_ftp_db_counts():
    """FTP와 DB의 이미지 개수 비교"""
    try:
        # FTP 파일 개수
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        
        ftp_counts = {}
        for category in CATEGORIES.keys():
            try:
                ftp.cwd(f'/homes/ha/sansam/{category}')
                files = []
                ftp.retrlines('NLST', files.append)
                ftp_counts[category] = len(files)
            except:
                ftp_counts[category] = 0
        
        ftp.quit()
        
        # DB 이미지 개수
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM gallery_images 
            GROUP BY category
        """)
        db_results = cursor.fetchall()
        db_counts = {row['category']: row['count'] for row in db_results}
        
        cursor.close()
        connection.close()
        
        # 비교
        print("\n  카테고리별 비교:")
        all_match = True
        for category, name in CATEGORIES.items():
            ftp_count = ftp_counts.get(category, 0)
            db_count = db_counts.get(category, 0)
            
            if ftp_count == db_count:
                print(f"    {name}: FTP {ftp_count}개 = DB {db_count}개 ✅")
            else:
                print(f"    {name}: FTP {ftp_count}개 ≠ DB {db_count}개 ⚠️")
                all_match = False
        
        if all_match:
            print("\n  ✅ FTP와 DB 데이터가 일치합니다!")
        else:
            print("\n  ⚠️  FTP와 DB 데이터가 일치하지 않습니다!")
            print("      → 이미지를 다시 업로드하거나 DB를 정리하세요.")
        
    except Exception as e:
        print(f"  ❌ 비교 실패: {e}")

# ============================================
# 실행
# ============================================
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 종료합니다.")
        sys.exit(0)
