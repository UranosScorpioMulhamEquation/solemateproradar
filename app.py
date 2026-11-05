import streamlit as st
import base64
from supabase import create_client, Client

# إعدادات الصفحة
st.set_page_config(
    page_title="مولد بيانات تراخيص الزبائن - استرو رادار",
    page_icon="🔑",
    layout="centered"
)

# دالة للاتصال والإضافة التلقائية لجدول Supabase
def add_customer_to_supabase(phone, key):
    try:
        url = st.secrets["SUPABASE_URL"]
        api_key = st.secrets["SUPABASE_KEY"]
        supabase: Client = create_client(url, api_key)

        # التحقق مما إذا كان رقم الهاتف مسجلاً مسبقاً
        response = supabase.table("licenses").select("phone").eq("phone", phone).execute()
        
        if len(response.data) > 0:
            return "exists"
        
        # إضافة الزبون الجديد بصف جديد مع ترك device_id فارغاً لكي يُسجل تلقائياً عبر الـ IP أول دخول
        supabase.table("licenses").insert({
            "phone": str(phone),
            "key": str(key),
            "device_id": ""
        }).execute()
        
        return True
    except Exception as e:
        return str(e)

# 1. نظام الحماية بكلمة المرور الرئيسية ("1981")
if 'master_auth' not in st.session_state:
    st.session_state['master_auth'] = False

if not st.session_state['master_auth']:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>🔐 بوابة الإدارة والتحكم - استرو رادار</h2>", unsafe_allow_html=True)
    st.info("هذه الصفحة مخصصة للمبرمج فقط ولا تفتح إلا بكلمة المرور السرية.")
    
    master_pwd = st.text_input("أدخل كلمة المرور السرية:", type="password")
    
    if st.button("دخول لوحة التحكم"):
        if master_pwd == "1981":
            st.session_state['master_auth'] = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة! حاول مرة أخرى.")
    st.stop()

# ==========================================================
# 🛠️ لوحة التحكم بعد نجاح الدخول بكلمة المرور "1981"
# ==========================================================
st.markdown("<h1 style='text-align: center;'>🪐 مولد بيانات التفعيل وشهادات الزبائن</h1>", unsafe_allow_html=True)
st.markdown("---")

st.write("أدخل بيانات الزبون أدناه لتوليد البيانات تلقائياً، إضافتها لقاعدة Supabase، واستخراج وثيقة الترخيص:")

# مدخلات بيانات الزبون
customer_name = st.text_input("👤 اسم الزبون الكريم:")
customer_phone = st.text_input("📱 رقم الهاتف (مثال: 12345685451):", placeholder="00971...")

if st.button("⚡ توليد الترخيص وحفظه سحابياً"):
    if customer_phone and customer_name:
        # استخراج الأرقام فقط وتطبيق المعادلة على الرقم كاملاً (بدون شرط الـ 8 أرقام)
        digits = ''.join(filter(str.isdigit, customer_phone))
        
        if not digits:
            st.error("⚠️ الرجاء إدخال رقم هاتف صحيح يحتوي على أرقام.")
        else:
            num = int(digits)
            activation_key = str(round(abs(num / 2 * 3.14)))[:6]

            # حفظ البيانات سحابياً في Supabase
            db_result = add_customer_to_supabase(customer_phone, activation_key)

            if db_result is True or db_result == "exists":
                if db_result == "exists":
                    st.warning("⚠️ رقم الهاتف موجود مسبقاً في قاعدة البيانات، وتم عرض بيانات الترخيص الخاصة به.")
                else:
                    st.success("✨ تم حفظ بيانات الزبون في قاعدة البيانات السحابية (Supabase) بنجاح!")

                # عرض النتائج في التطبيق بالترتيب: رقم الهاتف -> الرقم السري (بدون روابط)
                st.markdown("### 📋 ملخص بيانات الترخيص:")
                st.info(f"📱 **رقم الهاتف:** `{customer_phone}`")
                st.warning(f"🔑 **الرقم السري (مفتاح التفعيل):** `{activation_key}`")
                
                st.markdown("---")
                
                # تصميم صفحة HTML للترخيص (خالية من الروابط تماماً)
                html_content = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <title>شهادة ترخيص المنظومة الفلكية</title>
                    <style>
                        body {{
                            font-family: 'Cairo', Tahoma, sans-serif;
                            background-color: #f4f6f9;
                            padding: 40px;
                            direction: rtl;
                            text-align: right;
                        }}
                        .certificate {{
                            background: #ffffff;
                            padding: 40px;
                            border-radius: 16px;
                            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
                            max-width: 700px;
                            margin: auto;
                            border-top: 8px solid #6D28D9;
                            border-bottom: 8px solid #1e3a8a;
                        }}
                        h2 {{
                            color: #1e3a8a;
                            text-align: center;
                            font-size: 26px;
                            margin-bottom: 5px;
                        }}
                        .subtitle {{
                            text-align: center;
                            color: #666;
                            font-size: 14px;
                            margin-bottom: 30px;
                        }}
                        .info-group {{
                            font-size: 18px;
                            margin: 15px 0;
                            color: #333;
                        }}
                        .data-box {{
                            background: #f8fafc;
                            border: 2px solid #e2e8f0;
                            padding: 20px;
                            border-radius: 12px;
                            margin: 20px 0;
                        }}
                        .data-row {{
                            font-size: 18px;
                            margin: 16px 0;
                            color: #1e293b;
                        }}
                        .data-row strong {{
                            color: #1e3a8a;
                        }}
                        .instructions {{
                            background: #f0fdf4;
                            border-right: 4px solid #22c55e;
                            padding: 15px;
                            border-radius: 8px;
                            font-size: 15px;
                            color: #166534;
                            line-height: 1.6;
                            margin-top: 20px;
                        }}
                        .footer {{
                            text-align: center;
                            margin-top: 35px;
                            font-size: 14px;
                            color: #777;
                            border-top: 1px solid #eee;
                            padding-top: 15px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="certificate">
                        <h2>🪐 شهادة ترخيص استخدام المنظومة الفلكية</h2>
                        <div class="subtitle">صادرة رسمياً من منصة التحليلات الفلكية المطورة</div>
                        <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                        
                        <div class="info-group"><strong>اسم المستفيد (الزبون):</strong> {customer_name}</div>
                        
                        <div class="data-box">
                            <div class="data-row">📱 <strong>رقم الهاتف:</strong> {customer_phone}</div>
                            <div class="data-row" style="margin-top: 15px;">🔑 <strong>الرقم السري (مفتاح التفعيل):</strong> <span style="color: #6D28D9; font-weight: bold; letter-spacing: 2px;">{activation_key}</span></div>
                        </div>
                        
                        <div class="instructions">
                            <strong>📌 تعليمات التشغيل للزبون:</strong><br>
                            1. قم بفتح التطبيق الأساسي للمنظومة الفلكية.<br>
                            2. أدخل رقم هاتفك والرقم السري الموضح أعلاه في شاشة التفعيل لمرة واحدة فقط.<br>
                            3. سيتم قفل الترخيص تلقائياً على جهازك وشبكتك وتفتح المنظومة بكامل ميزاتها بشكل دائم.
                        </div>
                        
                        <div class="footer">
                            تم التطوير والاعتماد بواسطة: <strong>الباحث الفلكي استرو رادار (د. ملهم أحمد)</strong>
                        </div>
                    </div>
                </body>
                </html>
                """

                # معاينة الشهادة
                st.markdown("### 📄 معاينة وثيقة الترخيص الرسمية:")
                st.components.v1.html(html_content, height=550, scrolling=True)

                # زر تحميل الشهادة
                b64 = base64.b64encode(html_content.encode('utf-8')).decode("utf-8")
                href = f'''
                <div style="text-align: center; margin-top: 20px;">
                    <a href="data:text/html;base64,{b64}" download="License_Certificate_{customer_name}.html" 
                       style="display: inline-block; padding: 12px 25px; background-color: #6D28D9; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        📥 تحميل وثيقة الترخيص بصيغة HTML (جاهزة للطباعة أو الحفظ كـ PDF)
                    </a>
                </div>
                '''
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error(f"❌ حدث خطأ أثناء الاتصال بـ Supabase: {db_result}")
    else:
        st.warning("⚠️ الرجاء تعبئة اسم الزبون ورقم الهاتف بشكل صحيح أولاً.")
