"""
팜랜드 산양산삼 - DB/FTP 연결 테스트 스크립트

백엔드 서버 실행 전에 DB와 FTP 연결을 미리 테스트합니다.
"""

import mysql.connector
from mysql.connector import Error
import ftplib

# ============================================
# 설정
# ============================================
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'dodan1004~!@',
    'database': 'sansam'
}

FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/sansam/'
}

# ============================================
# 테스트 함수
# ============================================

def test_db_connection():
    """MySQL 데이터베이스 연결 테스트"""
    print("\n" + "="*60)
    print("🔍 MySQL 데이터베이스 연결 테스트")
    print("="*60)
    
    try:
        print(f"📡 연결 시도: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            print("✅ DB 연결 성공!")
            
            # 데이터베이스 정보 확인
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"   현재 DB: {db_name}")
            
            # 테이블 목록 확인
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"   테이블 개수: {len(tables)}")
            if tables:
                print("   테이블 목록:")
                for table in tables:
                    print(f"      - {table[0]}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"❌ DB 연결 실패: {e}")
        return False

def test_ftp_connection():
    """FTP 서버 연결 테스트"""
    print("\n" + "="*60)
    print("🔍 FTP 서버 연결 테스트")
    print("="*60)
    
    try:
        print(f"📡 연결 시도: {FTP_CONFIG['host']}:{FTP_CONFIG['port']}")
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        ftp.set_pasv(True)
        
        print("✅ FTP 연결 성공!")
        
        # 현재 디렉토리 확인
        current_dir = ftp.pwd()
        print(f"   현재 디렉토리: {current_dir}")
        
        # /sansam/ 폴더 확인
        try:
            ftp.cwd(FTP_CONFIG['base_path'])
            print(f"   ✅ 기본 폴더 존재: {FTP_CONFIG['base_path']}")
            
            # 하위 폴더 확인
            folders = []
            ftp.retrlines('LIST', lambda x: folders.append(x.split()[-1]))
            print(f"   하위 폴더 개수: {len(folders)}")
            if folders:
                print("   하위 폴더 목록:")
                for folder in folders:
                    print(f"      - {folder}")
        except:
            print(f"   ⚠️ 기본 폴더 없음: {FTP_CONFIG['base_path']}")
            print("   → 첫 업로드 시 자동 생성됩니다")
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"❌ FTP 연결 실패: {e}")
        return False

def test_gallery_images_table():
    """gallery_images 테이블 구조 확인"""
    print("\n" + "="*60)
    print("🔍 gallery_images 테이블 확인")
    print("="*60)
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 테이블 구조 확인
        cursor.execute("DESCRIBE gallery_images;")
        columns = cursor.fetchall()
        
        print("✅ 테이블 구조:")
        for col in columns:
            print(f"   {col[0]:20} {col[1]:15} NULL:{col[2]:3} KEY:{col[3]:3}")
        
        # 데이터 개수 확인
        cursor.execute("SELECT category, COUNT(*) FROM gallery_images GROUP BY category;")
        counts = cursor.fetchall()
        
        if counts:
            print("\n📊 카테고리별 이미지 개수:")
            for category, count in counts:
                print(f"   {category:10} {count}개")
        else:
            print("\n⚠️ 아직 업로드된 이미지가 없습니다")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ 테이블 확인 실패: {e}")
        return False

def test_products_table():
    """products 테이블 구조 확인"""
    print("\n" + "="*60)
    print("🔍 products 테이블 확인")
    print("="*60)
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 테이블 구조 확인
        cursor.execute("DESCRIBE products;")
        columns = cursor.fetchall()
        
        print("✅ 테이블 구조:")
        for col in columns:
            print(f"   {col[0]:20} {col[1]:15} NULL:{col[2]:3} KEY:{col[3]:3}")
        
        # 데이터 개수 확인
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1;")
        count = cursor.fetchone()[0]
        print(f"\n📊 등록된 상품: {count}개")
        
        if count > 0:
            cursor.execute("SELECT name, price FROM products WHERE is_active = 1;")
            products = cursor.fetchall()
            print("\n상품 목록:")
            for name, price in products:
                print(f"   {name} - {price:,}원")
        else:
            print("⚠️ 아직 등록된 상품이 없습니다")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ 테이블 확인 실패: {e}")
        return False

# ============================================
# 메인 실행
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌿 팜랜드 산양산삼 - 연결 테스트")
    print("="*60)
    
    results = []
    
    # 1. DB 연결 테스트
    results.append(("DB 연결", test_db_connection()))
    
    # 2. FTP 연결 테스트
    results.append(("FTP 연결", test_ftp_connection()))
    
    # 3. 테이블 확인
    if results[0][1]:  # DB 연결 성공 시에만
        results.append(("gallery_images 테이블", test_gallery_images_table()))
        results.append(("products 테이블", test_products_table()))
    
    # 최종 결과 요약
    print("\n" + "="*60)
    print("📊 테스트 결과 요약")
    print("="*60)
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    # 전체 성공 여부
    all_success = all([r[1] for r in results])
    
    print("\n" + "="*60)
    if all_success:
        print("🎉 모든 테스트 성공!")
        print("👉 이제 백엔드 서버를 실행하세요:")
        print("   서버실행_FastAPI.bat")
    else:
        print("⚠️ 일부 테스트 실패")
        print("👉 위의 에러 메시지를 확인하고 설정을 수정하세요")
    print("="*60 + "\n")
