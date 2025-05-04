# بيانات لعبة Dead by Daylight

# قائمة الكيلرز مع معلوماتهم
killers = [
    {
        "id": "trapper",
        "name": "ذا ترابر",
        "image": "static/images/killers/trapper.png",
        "difficulty": "سهل",
        "power": "لعبة الإله المدمرة",
        "backstory": "إيفان ماكميلان، المعروف باسم ذا ترابر، هو قاتل يستخدم مصائد الدب لإعاقة ضحاياه. كان ابن مالك منجم قاسي القلب، تعلم كيفية استخدام الوحشية للسيطرة على العمال."
    },
    {
        "id": "wraith",
        "name": "ذا رايث",
        "image": "static/images/killers/wraith.png",
        "difficulty": "متوسط",
        "power": "ريح الطائرة",
        "backstory": "فيليب أوجومو، المعروف باسم ذا رايث، لديه القدرة على التخفي والظهور بسرعة. كان ميكانيكيًا اكتشف أن رئيسه كان يقتل أشخاصًا وإخفاء جثثهم في السيارات المضغوطة."
    },
    {
        "id": "hillbilly",
        "name": "هيلبيلي",
        "image": "static/images/killers/hillbilly.png",
        "difficulty": "متوسط",
        "power": "ذا شينشاو",
        "backstory": "ماكس طومسون جونيور، المعروف باسم هيلبيلي، يستخدم منشارًا للهجوم. ولد بتشوهات وتم حبسه في غرفة علية من قبل والديه الذين كانوا يخجلون منه."
    },
    {
        "id": "nurse",
        "name": "ذا نيرس",
        "image": "static/images/killers/nurse.png",
        "difficulty": "صعب",
        "power": "سبينشر القطع",
        "backstory": "سالي سميثسون، المعروفة باسم ذا نيرس، تستخدم قدرات خارقة للطبيعة للانتقال عبر الأبعاد. كانت ممرضة في مصحة كوتون تجاهلها المجتمع بعد الحرب العالمية الأولى، مما أدى إلى انهيارها وقتل المرضى."
    },
    {
        "id": "huntress",
        "name": "ذا هانترس",
        "image": "static/images/killers/huntress.png",
        "difficulty": "متوسط",
        "power": "فؤوس الصيد",
        "backstory": "آنا، المعروفة باسم ذا هانترس، تستخدم فؤوس الرمي لقتل ضحاياها. عاشت حياتها في غابات شمال روسيا، وعندما ماتت والدتها، اضطرت للاعتماد على نفسها وأصبحت صيادة ماهرة."
    }
]

# قائمة السرفايفرز مع معلوماتهم
survivors = [
    {
        "id": "dwight",
        "name": "دوايت فيرفيلد",
        "image": "static/images/survivors/dwight.png",
        "difficulty": "سهل",
        "backstory": "دوايت كان دائمًا خارج المألوف ولم يكن لديه أصدقاء. في حفلة مع زملائه في العمل، قاموا بالمزاح معه وتركوه في الغابة وحيدًا، حيث اختفى في الضباب."
    },
    {
        "id": "meg",
        "name": "ميج توماس",
        "image": "static/images/survivors/meg.png",
        "difficulty": "متوسط",
        "backstory": "ميج كانت عداءة موهوبة وتنافسية. اضطرت لترك المدرسة والعودة إلى المنزل للعناية بوالدتها المريضة. كانت تركض في الغابة عندما اختفت في الضباب."
    },
    {
        "id": "claudette",
        "name": "كلوديت موريل",
        "image": "static/images/survivors/claudette.png",
        "difficulty": "سهل",
        "backstory": "كلوديت كانت خجولة وعاشقة للنباتات. كانت تستخدم الإنترنت للتواصل مع الآخرين وتعلم المزيد عن النباتات. ذهبت إلى الغابة للبحث عن نبات نادر عندما اختفت في الضباب."
    },
    {
        "id": "jake",
        "name": "جيك بارك",
        "image": "static/images/survivors/jake.png",
        "difficulty": "متوسط",
        "backstory": "جيك هو ابن رجل أعمال ثري، رفض حياة الثراء واختار العيش في الغابة وحيدًا. كان يعيش في كوخ صغير ويعتمد على نفسه عندما اختفى في الضباب."
    },
    {
        "id": "nea",
        "name": "نيا كارلسون",
        "image": "static/images/survivors/nea.png",
        "difficulty": "متوسط",
        "backstory": "نيا انتقلت من السويد إلى أمريكا مع عائلتها. كانت متمردة وتحب الرسم بالجرافيتي. في إحدى الليالي، كانت ترسم على جدار مبنى مهجور عندما اختفت في الضباب."
    }
]

# قائمة البيركس
perks = {
    "killer": [
        {
            "id": "bbq",
            "name": "باربكيو آند تشيلي",
            "image": "static/images/killers/Barbecue & Chilli.png",
            "description": "بعد تعليق سرفايفر، تظهر لك كل السرفايفرز الآخرين على بعد أكثر من 40 متر.",
            "character": "كانيبال"
        },
        {
            "id": "ruin",
            "name": "هيكس: روين",
            "image": "static/images/killers/Hex Ruin.png",
            "description": "كل مولدات الطاقة تتراجع بنسبة 200% عندما لا يصلحها أحد.",
            "character": "هاج"
        },
        {
            "id": "noed",
            "name": "هيكس: نو ون اسكيبس ديث",
            "image": "static/images/killers/Hex No One Escapes Death.png",
            "description": "بعد تشغيل كل المولدات، يعاني السرفايفرز من تأثير الوحشية ويمكنك إسقاطهم بضربة واحدة.",
            "character": "جميع الكيلرز"
        },
        {
            "id": "corrupt",
            "name": "كوراپت انترفنشن",
            "image": "static/images/killers/Corrupt Intervention.png",
            "description": "أبعد 3 مولدات عن السرفايفرز لمدة 120 ثانية في بداية المباراة.",
            "character": "بلاغو"
        },
        {
            "id": "pop",
            "name": "پوپ جوز ذا ويزل",
            "image": "static/images/killers/Pop Goes the Weasel.png",
            "description": "بعد تعليق سرفايفر، المولد التالي الذي تركله يفقد 25% من تقدمه.",
            "character": "كلاون"
        }
    ],
    "survivor": [
        {
            "id": "ds",
            "name": "ديسايسيف سترايك",
            "image": "static/images/perks/decisive_strike.png",
            "description": "بعد الإنقاذ من الخطاف، إذا حملك الكيلر، يمكنك طعنه والهروب.",
            "character": "لوري سترود"
        },
        {
            "id": "bt",
            "name": "بورود تايم",
            "image": "static/images/perks/borrowed_time.png",
            "description": "عند إنقاذ سرفايفر من الخطاف، يحصل على حماية ضد ضربة واحدة لمدة 15 ثانية.",
            "character": "بيل"
        },
        {
            "id": "dh",
            "name": "ديد هارد",
            "image": "static/images/perks/dead_hard.png",
            "description": "عندما تكون جريحًا، يمكنك الاندفاع للأمام وتجنب الضربة.",
            "character": "ديفيد كينج"
        },
        {
            "id": "sb",
            "name": "سپرنت بيرست",
            "image": "static/images/perks/sprint_burst.png",
            "description": "عندما تبدأ الركض، تحصل على تسارع كبير في السرعة لمدة 3 ثوانٍ.",
            "character": "ميج توماس"
        },
        {
            "id": "ub",
            "name": "أنبريكابل",
            "image": "static/images/perks/unbreakable.png",
            "description": "يمكنك التعافي من حالة الإصابة الخطيرة مرة واحدة في المباراة.",
            "character": "بيل"
        }
    ]
}

# دوال للحصول على بيانات محددة

def get_killer(killer_id):
    """الحصول على بيانات كيلر محدد بواسطة معرفه"""
    for killer in killers:
        if killer["id"] == killer_id:
            return killer
    return None

def get_survivor(survivor_id):
    """الحصول على بيانات سرفايفر محدد بواسطة معرفه"""
    for survivor in survivors:
        if survivor["id"] == survivor_id:
            return survivor
    return None

def get_killer_perks():
    """الحصول على جميع بيركس الكيلر"""
    return perks["killer"]

def get_survivor_perks():
    """الحصول على جميع بيركس السرفايفر"""
    return perks["survivor"]