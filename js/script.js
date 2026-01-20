// 팜랜드 산양산삼 랜딩 페이지 JavaScript

// ============================================
// Trust Grid Image Sliders
// ============================================
class TrustImageSlider {
    constructor(container, images) {
        this.container = container;
        this.images = images;
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        
        if (images.length > 0) {
            this.render();
            if (images.length > 1) {
                this.startAutoPlay();
            }
        }
    }
    
    render() {
        const hasMultiple = this.images.length > 1;
        
        this.container.innerHTML = `
            <div class="trust-image-slider">
                <div class="trust-image-track" data-slider-track>
                    ${this.images.map(img => `
                        <div class="trust-image-slide">
                            <img src="${img}" alt="Trust Image" loading="lazy">
                        </div>
                    `).join('')}
                </div>
                ${hasMultiple ? `
                    <button class="trust-slider-nav trust-slider-prev" data-slider-prev>‹</button>
                    <button class="trust-slider-nav trust-slider-next" data-slider-next>›</button>
                    <div class="trust-slider-indicators" data-slider-indicators>
                        ${this.images.map((_, i) => `
                            <button class="trust-slider-dot ${i === 0 ? 'active' : ''}" data-slider-dot="${i}"></button>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
        
        if (hasMultiple) {
            this.attachEvents();
        }
    }
    
    attachEvents() {
        const prevBtn = this.container.querySelector('[data-slider-prev]');
        const nextBtn = this.container.querySelector('[data-slider-next]');
        const dots = this.container.querySelectorAll('[data-slider-dot]');
        
        if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
        if (nextBtn) nextBtn.addEventListener('click', () => this.next());
        
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goTo(index));
        });
    }
    
    goTo(index) {
        this.currentIndex = index;
        const track = this.container.querySelector('[data-slider-track]');
        if (track) {
            track.style.transform = `translateX(-${index * 100}%)`;
        }
        
        this.updateIndicators();
        this.resetAutoPlay();
    }
    
    updateIndicators() {
        const dots = this.container.querySelectorAll('[data-slider-dot]');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }
    
    prev() {
        const newIndex = this.currentIndex > 0 ? this.currentIndex - 1 : this.images.length - 1;
        this.goTo(newIndex);
    }
    
    next() {
        const newIndex = this.currentIndex < this.images.length - 1 ? this.currentIndex + 1 : 0;
        this.goTo(newIndex);
    }
    
    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.next();
        }, 4000); // 4초마다 자동 넘김
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
        }
    }
    
    resetAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }
}

// ============================================
// 1. FAQ 아코디언
// ============================================
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // 현재 열려있는 다른 FAQ 닫기
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // 현재 FAQ 토글
            item.classList.toggle('active');
        });
    });
}

// ============================================
// 2. 스무스 스크롤
// ============================================
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            
            // 빈 href나 단순 # 는 제외
            if (href === '#' || href === '') return;
            
            e.preventDefault();
            
            const target = document.querySelector(href);
            if (target) {
                const headerHeight = document.getElementById('header').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ============================================
// 3. 폼 제출 처리
// ============================================
function initForms() {
    // 빠른 문의 폼
    const quickForm = document.getElementById('quickForm');
    if (quickForm) {
        quickForm.addEventListener('submit', handleQuickFormSubmit);
    }
    
    // 상세 문의 폼
    const detailForm = document.getElementById('detailForm');
    if (detailForm) {
        detailForm.addEventListener('submit', handleDetailFormSubmit);
    }
}

function handleQuickFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const phone = formData.get('phone');
    const purpose = formData.get('purpose');
    
    // 전화번호 유효성 검사
    if (!validatePhone(phone)) {
        alert('올바른 전화번호를 입력해 주세요.\n예: 010-0000-0000');
        return;
    }
    
    // SMS 전송 (기본 문자 앱 열기)
    const message = encodeURIComponent(`안녕하세요. 산양산삼 상담을 원합니다.\n문의 내용: ${purpose}\n연락처: ${phone}`);
    window.location.href = `sms:010-2512-6818?body=${message}`;
    
    // 폼 초기화 및 감사 메시지
    setTimeout(() => {
        e.target.reset();
        showThankYouMessage('간편 상담 신청이 완료되었습니다. 곧 연락드리겠습니다.');
    }, 500);
}

function handleDetailFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const name = formData.get('name');
    const phone = formData.get('phone');
    const purpose = formData.get('purpose');
    const budget = formData.get('budget') || '미정';
    const delivery = formData.get('delivery') || '미정';
    const message = formData.get('message') || '없음';
    
    // 전화번호 유효성 검사
    if (!validatePhone(phone)) {
        alert('올바른 전화번호를 입력해 주세요.\n예: 010-0000-0000');
        return;
    }
    
    // 개인정보 동의 확인
    if (!formData.get('privacy')) {
        alert('개인정보 수집 및 이용에 동의해 주세요.');
        return;
    }
    
    // SMS 전송 (기본 문자 앱 열기)
    const smsBody = encodeURIComponent(
        `[산양산삼 상담 신청]\n` +
        `이름: ${name}\n` +
        `연락처: ${phone}\n` +
        `목적: ${purpose}\n` +
        `예산: ${budget}\n` +
        `수령일: ${delivery}\n` +
        `추가요청: ${message}`
    );
    window.location.href = `sms:010-2512-6818?body=${smsBody}`;
    
    // 폼 초기화 및 감사 메시지
    setTimeout(() => {
        e.target.reset();
        showThankYouMessage('상세 상담 신청이 완료되었습니다. 확인 후 빠르게 연락드리겠습니다.');
        
        // 페이지 상단으로 스크롤
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }, 500);
}

// ============================================
// 4. 유틸리티 함수
// ============================================
function validatePhone(phone) {
    // 한국 전화번호 패턴 (010-0000-0000 또는 01000000000)
    const pattern = /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/;
    return pattern.test(phone.replace(/\s/g, ''));
}

function showThankYouMessage(message) {
    // 모달 생성
    const modal = document.createElement('div');
    modal.className = 'thank-you-modal';
    modal.innerHTML = `
        <div class="thank-you-content">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="16 8 10 14 8 12"></polyline>
            </svg>
            <h3>감사합니다!</h3>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="this.closest('.thank-you-modal').remove()">확인</button>
        </div>
    `;
    
    // 스타일 추가
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    const content = modal.querySelector('.thank-you-content');
    content.style.cssText = `
        background: white;
        padding: 40px;
        border-radius: 16px;
        max-width: 400px;
        text-align: center;
        animation: slideUp 0.3s ease;
    `;
    
    document.body.appendChild(modal);
    
    // 3초 후 자동 닫기
    setTimeout(() => {
        modal.remove();
    }, 5000);
}

// ============================================
// 5. 헤더 스크롤 효과
// ============================================
function initHeaderScroll() {
    const header = document.getElementById('header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.boxShadow = '0 4px 16px rgba(0,0,0,0.12)';
        } else {
            header.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        }
        
        lastScroll = currentScroll;
    });
}

// ============================================
// 6. 이미지 Lazy Loading (Placeholder 처리)
// ============================================
function initImagePlaceholders() {
    const placeholderImages = document.querySelectorAll('.placeholder-image');
    
    placeholderImages.forEach(img => {
        // 실제 이미지가 로드되지 않으면 placeholder 스타일 유지
        img.addEventListener('error', function() {
            this.style.background = 'linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%)';
            this.style.display = 'flex';
            this.style.alignItems = 'center';
            this.style.justifyContent = 'center';
            this.style.color = '#787878';
            this.style.fontSize = '14px';
            this.style.textAlign = 'center';
            this.style.padding = '20px';
        });
    });
}

// ============================================
// 7. 전화/문자 클릭 추적 (분석용)
// ============================================
function trackCTAClicks() {
    const callButtons = document.querySelectorAll('[href^="tel:"]');
    const smsButtons = document.querySelectorAll('[href^="sms:"]');
    
    callButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('전화 버튼 클릭:', btn.href);
            // Google Analytics 또는 기타 분석 도구 연동 가능
            // gtag('event', 'call_button_click', { ... });
        });
    });
    
    smsButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('문자 버튼 클릭:', btn.href);
            // Google Analytics 또는 기타 분석 도구 연동 가능
            // gtag('event', 'sms_button_click', { ... });
        });
    });
}

// ============================================
// 8. 폼 입력 자동 포맷팅 (전화번호)
// ============================================
function initPhoneFormatting() {
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/[^0-9]/g, '');
            
            if (value.length > 11) {
                value = value.substr(0, 11);
            }
            
            if (value.length > 6) {
                value = value.substr(0, 3) + '-' + value.substr(3, 4) + '-' + value.substr(7);
            } else if (value.length > 3) {
                value = value.substr(0, 3) + '-' + value.substr(3);
            }
            
            e.target.value = value;
        });
    });
}

// ============================================
// 9. 애니메이션 CSS 추가
// ============================================
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .thank-you-content svg {
            margin-bottom: 20px;
        }
        
        .thank-you-content h3 {
            font-size: 24px;
            font-weight: 700;
            color: #2d5016;
            margin-bottom: 12px;
        }
        
        .thank-you-content p {
            font-size: 16px;
            color: #5a5a5a;
            margin-bottom: 24px;
            line-height: 1.6;
        }
    `;
    document.head.appendChild(style);
}

// ============================================
// 9.5. 갤러리 & Lightbox (서버 API 방식)
// ============================================
const API_BASE = '/api/';
let currentCategoryImages = [];
let currentImageIndex = 0;

// Trust Grid 로드 (재배지, 년근구성, 선별, 배송)
async function loadTrustGrid() {
    const trustGrid = document.getElementById('trustGrid');
    if (!trustGrid) return;
    
    try {
        const response = await fetch(API_BASE + 'gallery');
        const result = await response.json();
        
        if (!result.success) {
            trustGrid.innerHTML = '<p style="text-align: center; color: #999;">갤러리를 불러올 수 없습니다</p>';
            return;
        }
        
        const galleryData = result.data;
        
        // 카테고리별 매핑
        const trustCategories = [
            { key: 'farm', title: '재배지', subtitle: '강원도 원주시 소초면 학곡리 산88', desc: '청정 자연환경에서 자라는 산양산삼' },
            { key: 'ginseng', title: '년근 구성', subtitle: '5~15년근 다양한 구성', desc: '뿌리 상태, 형태, 손상 여부 등을 기준으로 선별합니다' },
            { key: 'process', title: '선별 및 출고 기준', subtitle: '엄격한 품질 관리', desc: '수확 시기, 선별 과정, 포장 방식을 투명하게 공개합니다' },
            { key: 'package', title: '배송 및 보관 안내', subtitle: '신선도 유지 포장', desc: '계절별 최적 배송 방식으로 신선도를 유지합니다' }
        ];
        
        trustGrid.innerHTML = trustCategories.map(cat => {
            return `
                <div class="trust-item">
                    <div class="trust-image" data-trust-slider="${cat.key}">
                        <!-- Image slider will be initialized here -->
                    </div>
                    <div class="trust-content">
                        <h3>${cat.title}</h3>
                        <p><strong>${cat.subtitle}</strong></p>
                        <p class="trust-desc">${cat.desc}</p>
                    </div>
                </div>
            `;
        }).join('');
        
        // 각 카테고리의 이미지 슬라이더 초기화
        trustCategories.forEach(cat => {
            const container = trustGrid.querySelector(`[data-trust-slider="${cat.key}"]`);
            if (!container) return;
            
            const catData = galleryData[cat.key];
            let images = [];
            
            if (catData && catData.images && catData.images.length > 0) {
                // 실제 갤러리 이미지 사용
                images = catData.images.map(img => img.url);
            } else {
                // Placeholder 이미지
                images = [`data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect fill='%23e8f5e9' width='800' height='600'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%234caf50' font-size='24'%3E이미지 업로드 필요%3C/text%3E%3C/svg%3E`];
            }
            
            new TrustImageSlider(container, images);
        });
        
    } catch (error) {
        console.error('Trust Grid Load Error:', error);
        trustGrid.innerHTML = '<p style="text-align: center; color: #999;">갤러리를 불러올 수 없습니다</p>';
    }
}

async function loadGalleryImages() {
    const galleryGrid = document.getElementById('galleryGrid');
    if (!galleryGrid) return;
    
    try {
        // 서버 API에서 갤러리 데이터 불러오기
        const response = await fetch(API_BASE + 'gallery');
        const result = await response.json();
        
        if (!result.success) {
            console.error('Gallery Load Failed:', result.message);
            galleryGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999;">
                    <p style="font-size: 18px; margin-bottom: 10px;">⚠️ 갤러리 로드 실패</p>
                    <p style="font-size: 14px;">${result.message}</p>
                </div>
            `;
            return;
        }
        
        const galleryData = result.data;
        
        // 갤러리 HTML 생성
        galleryGrid.innerHTML = '';
        let hasImages = false;
        
        Object.keys(galleryData).forEach(category => {
            const catData = galleryData[category];
            if (catData.count === 0) return;
            
            hasImages = true;
            const repImage = catData.representative;
            
            const item = document.createElement('div');
            item.className = 'gallery-item';
            item.setAttribute('data-category', category);
            item.setAttribute('data-count', catData.count);
            
            item.innerHTML = `
                <img src="${repImage.url}" alt="${catData.name}" loading="lazy">
                <div class="gallery-overlay">
                    <span class="gallery-title">${catData.icon} ${catData.name}</span>
                    <span class="gallery-count">${catData.count}장</span>
                </div>
            `;
            
            galleryGrid.appendChild(item);
        });
        
        // 이미지가 하나도 없으면 안내 메시지
        if (!hasImages) {
            galleryGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999;">
                    <p style="font-size: 18px; margin-bottom: 10px;">📷 등록된 이미지가 없습니다</p>
                    <p style="font-size: 14px;">admin-server.php에서 이미지를 업로드해 주세요</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Gallery Load Error:', error);
        galleryGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999;">
                <p style="font-size: 18px; margin-bottom: 10px;">❌ 서버 연결 실패</p>
                <p style="font-size: 14px;">API 서버를 확인해 주세요</p>
            </div>
        `;
    }
}

function initGallery() {
    const galleryGrid = document.getElementById('galleryGrid');
    if (!galleryGrid) return;
    
    // 카테고리 클릭 이벤트 (이벤트 위임)
    galleryGrid.addEventListener('click', (e) => {
        const item = e.target.closest('.gallery-item');
        if (!item) return;
        
        const category = item.getAttribute('data-category');
        openCategoryLightbox(category);
    });
}

async function openCategoryLightbox(category) {
    try {
        const response = await fetch(API_BASE + `gallery?category=${category}`);
        const result = await response.json();
        
        if (!result.success || result.data.images.length === 0) return;
        
        currentCategoryImages = result.data.images;
        currentImageIndex = 0;
        showLightboxImage();
        
        const lightbox = document.getElementById('lightbox');
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    } catch (error) {
        console.error('Lightbox Open Error:', error);
    }
}

function showLightboxImage() {
    if (currentCategoryImages.length === 0) return;
    
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.querySelector('.lightbox-caption');
    const lightboxCounter = document.querySelector('.lightbox-counter');
    
    const currentImage = currentCategoryImages[currentImageIndex];
    
    lightboxImg.src = currentImage.url;
    lightboxCaption.textContent = currentImage.original_name;
    
    if (lightboxCounter) {
        lightboxCounter.textContent = `${currentImageIndex + 1} / ${currentCategoryImages.length}`;
    }
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
    currentCategoryImages = [];
    currentImageIndex = 0;
}

function initLightboxControls() {
    const lightbox = document.getElementById('lightbox');
    const closeBtn = document.querySelector('.lightbox-close');
    const prevBtn = document.querySelector('.lightbox-prev');
    const nextBtn = document.querySelector('.lightbox-next');
    
    if (!lightbox) return;
    
    // 닫기 버튼
    closeBtn.addEventListener('click', closeLightbox);
    
    // 배경 클릭 시 닫기
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    // ESC 키로 닫기
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });
    
    // 이전 이미지
    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (currentCategoryImages.length === 0) return;
        currentImageIndex = (currentImageIndex - 1 + currentCategoryImages.length) % currentCategoryImages.length;
        showLightboxImage();
    });
    
    // 다음 이미지
    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (currentCategoryImages.length === 0) return;
        currentImageIndex = (currentImageIndex + 1) % currentCategoryImages.length;
        showLightboxImage();
    });
    
    // 키보드 화살표로 이동
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (currentCategoryImages.length === 0) return;
        
        if (e.key === 'ArrowLeft') {
            prevBtn.click();
        } else if (e.key === 'ArrowRight') {
            nextBtn.click();
        }
    });
}

// ============================================
// 9. 인허가 갤러리 & 간단구매 로드
// ============================================

// 인허가 갤러리 로드
async function loadLicenseGallery() {
    const galleryGrid = document.getElementById('licenseGalleryGrid');
    if (!galleryGrid) return;
    
    try {
        const response = await fetch(API_BASE + 'gallery');
        const result = await response.json();
        
        if (!result.success || !result.data.license || result.data.license.count === 0) {
            // 데이터가 없을 때 안내 메시지 표시
            galleryGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📄</div>
                    <p style="font-size: 18px; margin-bottom: 10px;">아직 등록된 인허가 문서가 없습니다</p>
                    <p style="font-size: 14px;">관리자 페이지에서 인허가 이미지를 업로드해주세요</p>
                </div>
            `;
            return;
        }
        
        const licenseData = result.data.license;
        galleryGrid.innerHTML = '';
        
        licenseData.images.forEach((image, index) => {
            const item = document.createElement('div');
            item.className = 'gallery-item';
            item.innerHTML = `
                <img src="${image.url}" alt="${image.title || '인허가 문서'}" loading="lazy">
                <div class="gallery-overlay">
                    <span class="gallery-title">📄 ${image.title || '인허가 문서'}</span>
                </div>
            `;
            
            // 클릭 시 Lightbox로 큰 이미지 표시
            item.addEventListener('click', () => {
                openLicenseLightbox(licenseData.images, index);
            });
            
            galleryGrid.appendChild(item);
        });
        
    } catch (error) {
        console.error('License Gallery Load Error:', error);
        galleryGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #f44336;">
                <p style="font-size: 18px; margin-bottom: 10px;">⚠️ 인허가 갤러리 로드 실패</p>
                <p style="font-size: 14px;">${error.message}</p>
            </div>
        `;
    }
}

// 인허가 Lightbox 열기
function openLicenseLightbox(images, startIndex) {
    currentImages = images;
    currentImageIndex = startIndex;
    
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.querySelector('.lightbox-caption');
    
    lightbox.classList.add('active');
    lightboxImg.src = images[startIndex].url;
    lightboxCaption.textContent = images[startIndex].title || '인허가 문서';
    
    updateLightboxCounter();
}

// 간단구매 상품 로드
async function loadProducts() {
    const productGrid = document.getElementById('productGrid');
    if (!productGrid) return;
    
    try {
        const response = await fetch(API_BASE + 'products?active=1'); // 판매중인 상품만
        const result = await response.json();
        
        if (!result.success || result.data.length === 0) {
            // 데이터가 없을 때 안내 메시지 표시
            productGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999;">
                    <div style="font-size: 48px; margin-bottom: 16px;">🛒</div>
                    <p style="font-size: 18px; margin-bottom: 10px;">아직 등록된 상품이 없습니다</p>
                    <p style="font-size: 14px;">관리자 페이지에서 상품을 등록해주세요</p>
                </div>
            `;
            return;
        }
        
        productGrid.innerHTML = result.data.map(product => `
            <div class="product-card" onclick="goToPurchasePage(${product.id})">
                <img src="${product.image_path}" alt="${product.name}" class="product-image" 
                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27260%27 height=%27260%27%3E%3Crect fill=%27%23f0f0f0%27 width=%27260%27 height=%27260%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 dominant-baseline=%27middle%27 text-anchor=%27middle%27 fill=%27%23999%27 font-size=%2716%27%3E이미지 없음%3C/text%3E%3C/svg%3E'">
                <div class="product-info">
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">${Number(product.price).toLocaleString()}원</div>
                    ${product.description ? `<p class="product-description">${product.description}</p>` : ''}
                    <button class="product-buy-btn">🛒 구매하기</button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Products Load Error:', error);
        productGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #f44336;">
                <p style="font-size: 18px; margin-bottom: 10px;">⚠️ 상품 로드 실패</p>
                <p style="font-size: 14px;">${error.message}</p>
            </div>
        `;
    }
}

// 구매 페이지로 이동 (문의 폼으로 스크롤)
function goToPurchasePage(productId) {
    // 상품 정보 저장
    sessionStorage.setItem('selectedProductId', productId);
    
    // 문의 폼으로 스크롤
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // 1초 후 안내 메시지
        setTimeout(() => {
            alert('해당 상품에 대한 구매 문의를 아래 폼에 작성해주세요.\n\n☎️ 전화: 010-2512-6818\n💬 문자: 010-2512-6818');
        }, 500);
    } else {
        // 문의 폼이 없으면 직접 연락 안내
        alert('상품 구매 문의\n\n☎️ 전화: 010-2512-6818\n💬 문자: 010-2512-6818\n\n상담 시간: 08:00 ~ 20:00 (연중무휴)');
    }
}

// ============================================
// Live Timelapse Player
// ============================================

class LiveTimelapse {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.images = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.speed = 500; // ms per frame
        this.playInterval = null;
        
        this.init();
    }
    
    async init() {
        try {
            // FTP에서 Live 이미지 목록 가져오기
            const response = await fetch(API_BASE + 'live/images?limit=1000');
            const result = await response.json();
            
            if (!result.success || !result.data.images || result.data.images.length === 0) {
                this.showEmptyState();
                return;
            }
            
            this.images = result.data.images;
            this.currentIndex = 0;
            
            this.renderPlayer();
            this.loadImage(0);
            
            console.log(`✅ Live 타임랩스: ${this.images.length}개 이미지 로드 완료`);
        } catch (error) {
            console.error('Live Timelapse Load Error:', error);
            this.showEmptyState();
        }
    }
    
    renderPlayer() {
        this.container.innerHTML = `
            <div class="live-player-screen">
                <img id="liveImage" class="live-player-image" alt="Live Timelapse">
                <div class="live-info-overlay">
                    <span class="live-badge">🔴 LIVE</span>
                    <span class="live-image-counter" id="liveCounter">1 / ${this.images.length}</span>
                </div>
            </div>
            <div class="live-player-controls">
                <div class="live-progress-container" onclick="livePlayer.seekToPosition(event)">
                    <div class="live-progress-bar" id="liveProgress" style="width: 0%"></div>
                </div>
                <div class="live-controls-row">
                    <div class="live-controls-left">
                        <button class="live-btn live-btn-play" onclick="livePlayer.togglePlay()" id="livePlayBtn">
                            ▶️
                        </button>
                        <button class="live-btn" onclick="livePlayer.prev()" title="이전 프레임">
                            ⏮️
                        </button>
                        <button class="live-btn" onclick="livePlayer.next()" title="다음 프레임">
                            ⏭️
                        </button>
                        <span class="live-time-display" id="liveTime">0:00 / 0:00</span>
                    </div>
                    <div class="live-controls-right">
                        <div class="live-speed-control">
                            <span class="live-speed-label">속도</span>
                            <button class="live-speed-btn" onclick="livePlayer.setSpeed(1000)">0.5x</button>
                            <button class="live-speed-btn active" onclick="livePlayer.setSpeed(500)">1x</button>
                            <button class="live-speed-btn" onclick="livePlayer.setSpeed(250)">2x</button>
                            <button class="live-speed-btn" onclick="livePlayer.setSpeed(100)">5x</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    loadImage(index) {
        if (index < 0 || index >= this.images.length) return;
        
        this.currentIndex = index;
        const img = document.getElementById('liveImage');
        if (img) {
            img.src = this.images[index].url;
        }
        
        this.updateUI();
    }
    
    updateUI() {
        // Progress bar
        const progress = document.getElementById('liveProgress');
        if (progress) {
            const percent = (this.currentIndex / (this.images.length - 1)) * 100;
            progress.style.width = `${percent}%`;
        }
        
        // Counter
        const counter = document.getElementById('liveCounter');
        if (counter) {
            counter.textContent = `${this.currentIndex + 1} / ${this.images.length}`;
        }
        
        // Time display (예상 시간 계산)
        const time = document.getElementById('liveTime');
        if (time) {
            const currentTime = Math.floor(this.currentIndex * this.speed / 1000);
            const totalTime = Math.floor(this.images.length * this.speed / 1000);
            time.textContent = `${this.formatTime(currentTime)} / ${this.formatTime(totalTime)}`;
        }
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    togglePlay() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    play() {
        this.isPlaying = true;
        const playBtn = document.getElementById('livePlayBtn');
        if (playBtn) playBtn.textContent = '⏸️';
        
        this.playInterval = setInterval(() => {
            if (this.currentIndex < this.images.length - 1) {
                this.loadImage(this.currentIndex + 1);
            } else {
                // 마지막 프레임이면 처음으로
                this.loadImage(0);
            }
        }, this.speed);
    }
    
    pause() {
        this.isPlaying = false;
        const playBtn = document.getElementById('livePlayBtn');
        if (playBtn) playBtn.textContent = '▶️';
        
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
    }
    
    next() {
        this.pause();
        if (this.currentIndex < this.images.length - 1) {
            this.loadImage(this.currentIndex + 1);
        } else {
            this.loadImage(0);
        }
    }
    
    prev() {
        this.pause();
        if (this.currentIndex > 0) {
            this.loadImage(this.currentIndex - 1);
        } else {
            this.loadImage(this.images.length - 1);
        }
    }
    
    setSpeed(speed) {
        this.speed = speed;
        
        // 속도 버튼 활성화 상태 업데이트
        document.querySelectorAll('.live-speed-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // 재생 중이면 재시작
        if (this.isPlaying) {
            this.pause();
            this.play();
        }
    }
    
    seekToPosition(event) {
        const rect = event.currentTarget.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const percent = x / rect.width;
        const newIndex = Math.floor(percent * this.images.length);
        
        this.pause();
        this.loadImage(newIndex);
    }
    
    showEmptyState() {
        this.container.innerHTML = `
            <div class="live-empty-state">
                <div class="live-empty-icon">📹</div>
                <div class="live-empty-text">타임랩스 이미지가 없습니다</div>
                <div class="live-empty-subtext">FTP의 /live/ 폴더에 이미지가 쌓이면 자동으로 표시됩니다</div>
            </div>
        `;
    }
}

// Live Player 인스턴스
let livePlayer = null;

// ============================================
// 10. 초기화
// ============================================

// 버전 정보 로드
async function loadVersion() {
    try {
        const response = await fetch(API_BASE + 'version');
        const result = await response.json();
        
        if (result.success) {
            const versionEl = document.getElementById('versionInfo');
            if (versionEl) {
                versionEl.textContent = `v${result.version}`;
                versionEl.title = `${result.description} (${result.version_date})`;
            }
        }
    } catch (error) {
        console.error('Version Load Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadVersion(); // 버전 정보 로드
    loadTrustGrid(); // Trust Grid (재배지, 년근구성, 선별, 배송) 로드
    loadGalleryImages(); // 갤러리 이미지를 먼저 로드
    livePlayer = new LiveTimelapse('livePlayer'); // Live 타임랩스 초기화
    loadLicenseGallery(); // 인허가 갤러리 로드
    loadProducts(); // 간단구매 상품 로드
    initFAQ();
    initSmoothScroll();
    initForms();
    initHeaderScroll();
    initImagePlaceholders();
    trackCTAClicks();
    initPhoneFormatting();
    addAnimationStyles();
    initGallery(); // 갤러리 클릭 이벤트
    initLightboxControls(); // Lightbox 컨트롤
    
    console.log('팜랜드 산양산삼 랜딩 페이지 초기화 완료');
});

// ============================================
// 11. 외부 노출 API (필요시 사용)
// ============================================
window.ChamLand = {
    version: '1.0.0',
    contact: {
        phone: '010-2512-6818',
        hours: '08:00~20:00'
    }
};
