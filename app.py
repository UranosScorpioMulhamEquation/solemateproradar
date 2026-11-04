import streamlit as st
import base64

# إعدادات الصفحة
st.set_page_config(
    page_title="مولد مفاتيح تراخيص الزبائن - استرو رادار",
    page_icon="🔑",
    layout="centered"
)

# 1. نظام الحماية بكلمة المرور الرئيسية (خاصة بك وحدك "1981")
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
st.markdown("<h1 style='text-align: center;'>🪐 مولد مفاتيح التوريد وشهادات الزبائن</h1>", unsafe_allow_html=True)
st.markdown("---")

st.write("أدخل بيانات الزبون أدناه لتوليد مفتاح التفعيل الخاص به واستخراج وثيقة الترخيص:")

# مدخلات بيانات الزبون
customer_name = st.text_input("👤 اسم الزبون الكريم:")
customer_phone = st.text_input("📱 رقم الهاتف بصيغة الدولة (مثال: 00971501234567):", placeholder="00971...")

if st.button("⚡ توليد مفتاح التفعيل ووثيقة الترخيص"):
    if customer_phone and customer_name:
        # تطبيق المعادلة الرياضية المخصصة
        digits = ''.join(filter(str.isdigit, customer_phone))
        
        if len(digits) < 8:
            st.error("⚠️ رقم الهاتف المدخل قصير جداً، يجب أن يحتوي على أرقام كافية لتطبيق المعادلة.")
        else:
            num = int(digits[:8])
            activation_key = str(round(abs(num / 2 * 3.14)))[:6]

            st.success("تم توليد المفتاح بنجاح!")
            
            # عرض النتيجة بشكل بارز
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="رقم الهاتف المعرّف", value=customer_phone)
            with col2:
                st.metric(label="مفتاح التفعيل (نسخه للزبون)", value=activation_key)
            
            st.markdown("---")
            
            # تصميم صفحة HTML احترافية للترخيص قابلة للتحويل لـ PDF
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
                    .key-display {{
                        background: #f8fafc;
                        border: 2px dashed #6D28D9;
                        padding: 20px;
                        border-radius: 12px;
                        text-align: center;
                        font-size: 32px;
                        font-weight: bold;
                        color: #6D28D9;
                        letter-spacing: 5px;
                        margin: 25px 0;
                    }}
                    .instructions {{
                        background: #eff6ff;
                        padding: 15px;
                        border-radius: 8px;
                        font-size: 14px;
                        color: #1e40af;
                        line-height: 1.6;
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
                    <div class="info-group"><strong>رقم الهاتف المعتمد:</strong> {customer_phone}</div>
                    
                    <p style="margin-top: 25px; font-size: 16px;">تم إصدار مفتاح التفعيل الخاص بك لضمان تشغيل المنظومة بكفاءة تامة لمدة 5 سنوات:</p>
                    
                    <div class="key-display">{activation_key}</div>
                    
                    <div class="instructions">
                        <strong>📌 تعليمات التشغيل للزبون:</strong><br>
                        1. افتح رابط المنظومة الفلكية على هاتفك.<br>
                        2. عند ظهور شاشة التفعيل لأول مرة، أدخل رقم هاتفك الأعلى <b>{customer_phone}</b> ومفتاح التفعيل الموضح أعلاه.<br>
                        3. يتم حفظ التفعيل في متصفح هاتفك تلقائياً لمدة 5 سنوات كاملة.
                    </div>
                    
                    <div class="footer">
                        تم التطوير والاعتماد بواسطة: <strong>الباحث الفلكي استرو رادار (د. ملهم أحمد)</strong>
                    </div>
                </div>
            </body>
            </html>
            """

            # معاينة الشهادة داخل التطبيق
            st.markdown("### 📄 معاينة وثيقة الترخيص الرسمية:")
            st.components.v1.html(html_content, height=520, scrolling=True)

            # زر تحميل ملف HTML (والذي يمكن فتحه بالمتصفح وضغط Ctrl+P ثم الحفظ كـ PDF بإذن الله)
            b64 = base64.b64encode(html_content.encode('utf-8')).decode("utf-8")
            href = f'''
            <div style="text-align: center; margin-top: 20px;">
                <a href="data:text/html;base64,{b64}" download="License_Certificate_{customer_name}.html" 
                   style="display: inline-block; padding: 12px 25px; background-color: #6D28D9; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                   📥 تحميل وثيقة الترخيص (HTML جاهزة للطباعة أو التحويل لـ PDF)
                </a>
            </div>
            '''
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ الرجاء تعبئة اسم الزبون ورقم الهاتف بشكل صحيح أولاً.")