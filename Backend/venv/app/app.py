import streamlit as st
import requests

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Hospital AI Agent",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Hospital AI Agent Assistant")
st.write("مرحباً بك! يمكنك التواصل مع الـ Hospital AI Agent مباشرة من هنا.")

API_URL = "http://127.0.0.1:8000/agent/chat"

# 2. تهيئة ذاكرة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال السؤال وإرساله
if prompt := st.chat_input("اكتب سؤالك أو استفسارك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري التواصل مع الـ Agent..."):
            try:
                # إرسال المفتاح المطابق للـ Backend (prompt)
                response_data = requests.post(
                    API_URL, 
                    json={"prompt": prompt}, 
                    timeout=60
                )
                
                if response_data.status_code == 200:
                    result = response_data.json()
                    
                    if isinstance(result, dict):
                        # استخراج الرد المباشر من المفتاح response
                        bot_response = result.get("response") or result.get("reply") or result.get("message")
                        
                        # في حالة إرجاع قيمة فارغة من الـ Backend
                        if not bot_response:
                            bot_response = "⚠️ لم يتم استلام رد من الـ Agent. تأكدي من ضبط API Key أو قواعد البيانات في الـ Backend."
                    else:
                        bot_response = str(result)
                else:
                    bot_response = f"⚠️ خطأ في الاتصال بالسيرفر: (كود الخطأ {response_data.status_code})"
                    
            except requests.exceptions.ConnectionError:
                bot_response = "❌ تعذر الاتصال بالـ Backend! تأكدي من أن سيرفر FastAPI يعمل."
            except Exception as e:
                bot_response = f"⚠️ حدث خطأ غير متوقع: {str(e)}"

            st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})