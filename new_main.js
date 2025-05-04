/**
 * ملف JavaScript الرئيسي للموقع الجديد
 */

document.addEventListener('DOMContentLoaded', function() {
    // تفعيل tooltips من Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // تفعيل Popover من Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // تنفيذ البحث في الكيلرز
    setupSearch('killer-search', 'killer-card');

    // تنفيذ البحث في السرفايفرز
    setupSearch('survivor-search', 'survivor-card');

    // تنفيذ البحث في البيركس
    setupSearch('perk-search', 'perk-card');

    // تنفيذ تصفية الكيلرز حسب الصعوبة
    setupFilter('killer-difficulty-filter', 'killer-card', 'data-difficulty');

    // تنفيذ تصفية السرفايفرز حسب الصعوبة
    setupFilter('survivor-difficulty-filter', 'survivor-card', 'data-difficulty');

    // نموذج الاشتراك في النشرة الإخبارية
    setupNewsletterForm();
});

/**
 * دالة لإعداد وظيفة البحث
 * @param {string} searchInputId - معرّف عنصر input للبحث
 * @param {string} cardClass - الفئة التي تحدد البطاقات التي سيتم البحث فيها
 */
function setupSearch(searchInputId, cardClass) {
    const searchInput = document.getElementById(searchInputId);
    
    // الخروج إذا لم يكن عنصر البحث موجودًا في الصفحة الحالية
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchText = this.value.trim().toLowerCase();
        filterCards(cardClass, searchText);
    });
}

/**
 * تصفية البطاقات بناءً على نص البحث
 * @param {string} cardClass - الفئة التي تحدد البطاقات التي سيتم تصفيتها
 * @param {string} searchText - نص البحث
 */
function filterCards(cardClass, searchText) {
    const cards = document.getElementsByClassName(cardClass);
    
    for (let card of cards) {
        const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
        const cardText = card.querySelector('.card-text') ? 
                        card.querySelector('.card-text').textContent.toLowerCase() : '';
        
        if (cardTitle.includes(searchText) || cardText.includes(searchText)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    }
}

/**
 * دالة لإعداد وظيفة التصفية
 * @param {string} filterId - معرّف عنصر القائمة المنسدلة للتصفية
 * @param {string} cardClass - الفئة التي تحدد البطاقات التي سيتم تصفيتها
 * @param {string} dataAttribute - سمة البيانات التي سيتم التصفية حسبها
 */
function setupFilter(filterId, cardClass, dataAttribute) {
    const filterSelect = document.getElementById(filterId);
    
    // الخروج إذا لم يكن عنصر التصفية موجودًا في الصفحة الحالية
    if (!filterSelect) return;
    
    filterSelect.addEventListener('change', function() {
        const filterValue = this.value;
        const cards = document.getElementsByClassName(cardClass);
        
        for (let card of cards) {
            if (filterValue === 'all' || card.getAttribute(dataAttribute) === filterValue) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

/**
 * دالة لإعداد نموذج الاشتراك في النشرة الإخبارية
 */
function setupNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    // الخروج إذا لم يكن نموذج النشرة الإخبارية موجودًا في الصفحة الحالية
    if (!newsletterForm) return;
    
    newsletterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const emailInput = this.querySelector('input[type="email"]');
        const email = emailInput.value.trim();
        
        if (validateEmail(email)) {
            // هنا يمكن إضافة كود لإرسال البريد الإلكتروني إلى الخادم
            // عرض رسالة نجاح
            showToast('تم الاشتراك بنجاح! شكرًا لك.', 'success');
            emailInput.value = '';
        } else {
            showToast('يرجى إدخال عنوان بريد إلكتروني صالح.', 'danger');
        }
    });
}

/**
 * التحقق من صحة البريد الإلكتروني
 * @param {string} email - البريد الإلكتروني المراد التحقق منه
 * @returns {boolean} - صحيح إذا كان البريد الإلكتروني صالحًا
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * عرض رسالة toast للمستخدم
 * @param {string} message - الرسالة التي سيتم عرضها
 * @param {string} type - نوع الرسالة (success, danger, warning)
 */
function showToast(message, type) {
    // إنشاء عنصر toast
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    
    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');
    
    const toastFlex = document.createElement('div');
    toastFlex.className = 'd-flex';
    
    const toastBody = document.createElement('div');
    toastBody.className = 'toast-body';
    toastBody.textContent = message;
    
    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close btn-close-white me-2 m-auto';
    closeButton.setAttribute('data-bs-dismiss', 'toast');
    closeButton.setAttribute('aria-label', 'إغلاق');
    
    // بناء هيكل الـ toast
    toastFlex.appendChild(toastBody);
    toastFlex.appendChild(closeButton);
    toastElement.appendChild(toastFlex);
    toastContainer.appendChild(toastElement);
    
    // إضافة الـ toast إلى الصفحة
    document.body.appendChild(toastContainer);
    
    // تهيئة وإظهار الـ toast
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // إزالة الـ toast من الصفحة بعد إغلاقه
    toastElement.addEventListener('hidden.bs.toast', function() {
        document.body.removeChild(toastContainer);
    });
}