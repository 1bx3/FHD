from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
import os
import data

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index_new.html')

# صفحة الكيلرز
@app.route('/killers')
def killers_page():
    all_killers = data.killers
    return render_template('killers_new.html', killers=all_killers)

# صفحة تفاصيل الكيلر
@app.route('/killers/<killer_id>')
def killer_details(killer_id):
    killer = data.get_killer(killer_id)
    if not killer:
        abort(404)
    return render_template('killer_details_new.html', killer=killer)

# صفحة السرفايفرز
@app.route('/survivors')
def survivors_page():
    all_survivors = data.survivors
    return render_template('survivors_new.html', survivors=all_survivors)

# صفحة تفاصيل السرفايفر
@app.route('/survivors/<survivor_id>')
def survivor_details(survivor_id):
    survivor = data.get_survivor(survivor_id)
    if not survivor:
        abort(404)
    return render_template('survivor_details_new.html', survivor=survivor)

# صفحة البيركس
@app.route('/perks')
def perks_page():
    killer_perks = data.get_killer_perks()
    survivor_perks = data.get_survivor_perks()
    return render_template('perks_new.html', killer_perks=killer_perks, survivor_perks=survivor_perks)

# صفحة الإحصائيات
@app.route('/stats')
def stats_page():
    # هنا يمكن إضافة بيانات الإحصائيات لاحقًا
    return render_template('stats_new.html')

# صفحة دليل المبتدئين
@app.route('/guide')
def guide_page():
    return render_template('guide_new.html')

# معالجة الاشتراك في النشرة الإخبارية
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.form.get('email')
        # هنا يمكن إضافة كود لحفظ البريد الإلكتروني في قاعدة البيانات
        return jsonify({'success': True, 'message': 'تم الاشتراك بنجاح!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'حدث خطأ: {str(e)}'})

# صفحة 404 - الصفحة غير موجودة
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404_new.html'), 404

# صفحة 500 - خطأ في الخادم
@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500_new.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)