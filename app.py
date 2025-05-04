import os
from flask import Flask, render_template, request, abort

# استيراد بيانات اللعبة
from data import killers, survivors, perks, get_killer, get_survivor, get_killer_perks, get_survivor_perks

# إنشاء تطبيق Flask
app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# صفحة الكيلرز
@app.route('/killers')
def killers_page():
    return render_template('killers.html', killers=killers)

# صفحة تفاصيل الكيلر
@app.route('/killers/<killer_id>')
def killer_details(killer_id):
    killer = get_killer(killer_id)
    if not killer:
        abort(404)
    return render_template('killer_details.html', killer=killer)

# صفحة السرفايفرز
@app.route('/survivors')
def survivors_page():
    return render_template('survivors.html', survivors=survivors)

# صفحة تفاصيل السرفايفر
@app.route('/survivors/<survivor_id>')
def survivor_details(survivor_id):
    survivor = get_survivor(survivor_id)
    if not survivor:
        abort(404)
    return render_template('survivor_details.html', survivor=survivor)

# صفحة البيركس
@app.route('/perks')
def perks_page():
    killer_perks = get_killer_perks()
    survivor_perks = get_survivor_perks()
    return render_template('perks.html', killer_perks=killer_perks, survivor_perks=survivor_perks)

# صفحة الإحصائيات
@app.route('/stats')
def stats_page():
    return render_template('stats.html')

# معالج الخطأ 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error="الصفحة غير موجودة"), 404

# معالج الخطأ 500
@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', error="حدث خطأ في الخادم"), 500