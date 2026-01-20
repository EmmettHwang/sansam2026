-- sansam 데이터베이스 테이블 생성 SQL

-- 1. 갤러리 이미지 테이블
CREATE TABLE IF NOT EXISTS `gallery_images` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category` VARCHAR(50) NOT NULL COMMENT '카테고리 (farm, ginseng, process, package, license)',
    `filename` VARCHAR(255) NOT NULL COMMENT '파일명',
    `original_name` VARCHAR(255) NOT NULL COMMENT '원본 파일명',
    `file_path` VARCHAR(500) NOT NULL COMMENT 'FTP 경로',
    `file_size` INT NOT NULL COMMENT '파일 크기 (bytes)',
    `width` INT DEFAULT NULL COMMENT '이미지 너비',
    `height` INT DEFAULT NULL COMMENT '이미지 높이',
    `is_representative` TINYINT(1) DEFAULT 0 COMMENT '대표 이미지 여부',
    `display_order` INT DEFAULT 0 COMMENT '표시 순서',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_category` (`category`),
    INDEX `idx_representative` (`is_representative`),
    INDEX `idx_order` (`display_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='갤러리 이미지';

-- 2. 카테고리 설정 테이블 (선택 사항)
CREATE TABLE IF NOT EXISTS `gallery_categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(50) NOT NULL UNIQUE COMMENT '카테고리 코드',
    `name` VARCHAR(100) NOT NULL COMMENT '카테고리 이름',
    `icon` VARCHAR(50) DEFAULT NULL COMMENT '아이콘',
    `display_order` INT DEFAULT 0 COMMENT '표시 순서',
    `is_active` TINYINT(1) DEFAULT 1 COMMENT '활성화 여부',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_code` (`code`),
    INDEX `idx_order` (`display_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='갤러리 카테고리';

-- 기본 카테고리 데이터 삽입
INSERT INTO `gallery_categories` (`code`, `name`, `icon`, `display_order`) VALUES
('farm', '재배지', '🏞️', 1),
('ginseng', '산양산삼', '🌿', 2),
('process', '선별과정', '⚙️', 3),
('package', '포장', '📦', 4),
('license', '인허가', '📄', 5)
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 3. 상품 테이블 (간단구매용)
CREATE TABLE IF NOT EXISTS `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(200) NOT NULL COMMENT '상품명',
    `description` TEXT DEFAULT NULL COMMENT '상품 설명',
    `price` INT NOT NULL COMMENT '가격 (원)',
    `image_path` VARCHAR(500) NOT NULL COMMENT '상품 이미지 경로',
    `stock` INT DEFAULT 999 COMMENT '재고 (999=무제한)',
    `display_order` INT DEFAULT 0 COMMENT '표시 순서',
    `is_active` TINYINT(1) DEFAULT 1 COMMENT '판매 활성화',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_active` (`is_active`),
    INDEX `idx_order` (`display_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='상품';

-- 4. 주문 테이블
CREATE TABLE IF NOT EXISTS `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_number` VARCHAR(50) NOT NULL UNIQUE COMMENT '주문번호',
    `product_id` INT NOT NULL COMMENT '상품 ID',
    `product_name` VARCHAR(200) NOT NULL COMMENT '상품명 (스냅샷)',
    `product_price` INT NOT NULL COMMENT '상품 가격 (스냅샷)',
    `quantity` INT NOT NULL DEFAULT 1 COMMENT '수량',
    `total_price` INT NOT NULL COMMENT '총 금액',
    `customer_name` VARCHAR(100) NOT NULL COMMENT '구매자명',
    `customer_phone` VARCHAR(20) NOT NULL COMMENT '연락처',
    `customer_email` VARCHAR(200) DEFAULT NULL COMMENT '이메일',
    `delivery_address` TEXT NOT NULL COMMENT '배송지 주소',
    `delivery_message` TEXT DEFAULT NULL COMMENT '배송 메시지',
    `payment_status` VARCHAR(20) DEFAULT 'pending' COMMENT '결제 상태 (pending, confirmed, cancelled)',
    `order_status` VARCHAR(20) DEFAULT 'ordered' COMMENT '주문 상태 (ordered, shipped, delivered, cancelled)',
    `ip_address` VARCHAR(45) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_order_number` (`order_number`),
    INDEX `idx_product` (`product_id`),
    INDEX `idx_payment_status` (`payment_status`),
    INDEX `idx_order_status` (`order_status`),
    INDEX `idx_created` (`created_at`),
    FOREIGN KEY (`product_id`) REFERENCES `products`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='주문';

-- 5. 업로드 로그 테이블 (선택 사항 - 디버깅용)
CREATE TABLE IF NOT EXISTS `upload_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category` VARCHAR(50) NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `status` VARCHAR(50) NOT NULL COMMENT 'success, failed',
    `error_message` TEXT DEFAULT NULL,
    `ip_address` VARCHAR(45) DEFAULT NULL,
    `user_agent` VARCHAR(500) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_status` (`status`),
    INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='업로드 로그';
