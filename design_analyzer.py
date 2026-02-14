import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Page config
st.set_page_config(page_title="تحلیلگر طراحی هوش مصنوعی", page_icon="🎨", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Vazirmatn', Tahoma, Arial, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .sub-header {
        text-align: center !important;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
    }
    
    .principle-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-right: 5px solid;
    }
    
    .principle-good {
        border-color: #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    }
    
    .principle-needs-work {
        border-color: #ffc107;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    }
    
    .principle-poor {
        border-color: #dc3545;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    }
    
    .optimization-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 2px solid #667eea;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎨 تحلیلگر طراحی با هوش مصنوعی</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">لوگوی خود را آپلود کنید و تحلیل حرفه‌ای دریافت کنید</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.write("### تنظیمات")
    st.write("#### کلید API گوگل جمینای")
    st.write("مراحل دریافت:")
    st.write("- به aistudio.google.com بروید")
    st.write("- با حساب گوگل وارد شوید")  
    st.write("- کلید جدید بسازید")
    
    gemini_api_key = st.text_input("کلید API", type="password")
    
    st.write("---")
    st.write("#### اصول طراحی")
    st.write("✓ تعادل و ترکیب‌بندی")
    st.write("✓ تئوری رنگ")
    st.write("✓ تایپوگرافی")
    st.write("✓ کنتراست")
    st.write("✓ مقیاس‌پذیری")
    st.write("✓ سلسله‌مراتب")

# Main
if not gemini_api_key:
    st.info("لطفاً کلید API خود را در نوار کناری وارد کنید")
    st.stop()

try:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("کلید API نامعتبر است")
    st.stop()

uploaded_file = st.file_uploader("فایل لوگو را آپلود کنید", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### طراحی شما")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    
    with col2:
        st.write("### تمرکز بهینه‌سازی")
        
        focus_minimalism = st.checkbox("مینیمالیسم و سادگی")
        focus_accessibility = st.checkbox("دسترسی‌پذیری")
        focus_modern = st.checkbox("ترندهای مدرن")
        focus_color = st.checkbox("هارمونی رنگی")
        focus_scalability = st.checkbox("مقیاس‌پذیری")
    
    focus_areas = []
    if focus_minimalism: focus_areas.append("مینیمالیسم")
    if focus_accessibility: focus_areas.append("دسترسی‌پذیری")
    if focus_modern: focus_areas.append("ترندهای مدرن")
    if focus_color: focus_areas.append("هارمونی رنگی")
    if focus_scalability: focus_areas.append("مقیاس‌پذیری")
    
    focus_instruction = ""
    if focus_areas:
        focus_instruction = f"\n\nموارد مهم: {', '.join(focus_areas)}"
    
    st.write("---")
    
    if st.button("شروع تحلیل"):
        with st.spinner("در حال تحلیل..."):
            try:
                uploaded_file.seek(0)
                image = Image.open(uploaded_file)
                
                prompt = f"""تحلیل طراحی این لوگو به فرمت JSON (فارسی):

{{
    "overall_score": <1-10>,
    "summary": "<خلاصه>",
    "principles": [
        {{
            "name": "<نام>",
            "status": "<good/needs-work/poor>",
            "score": <1-10>,
            "feedback": "<بازخورد>"
        }}
    ],
    "optimizations": [
        {{
            "version": "<نام>",
            "focus": "<تمرکز>",
            "visual_description": "<توصیف>",
            "implementation_steps": ["<مرحله>"],
            "changes": [
                {{
                    "aspect": "<جنبه>",
                    "reason": "<دلیل>",
                    "improvement": "<بهبود>",
                    "specific_instructions": "<دستورالعمل>"
                }}
            ],
            "description": "<توضیح>"
        }}
    ]
}}

اصول: تعادل، رنگ، تایپوگرافی، کنتراست، مقیاس‌پذیری، سلسله‌مراتب

3 پیشنهاد بده.{focus_instruction}"""

                response = model.generate_content([prompt, image])
                response_text = response.text
                
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(response_text.strip())
                st.session_state.analysis = analysis
                
            except Exception as e:
                st.error(f"خطا: {str(e)}")
                st.stop()
        
        st.success("تحلیل انجام شد")
        st.rerun()

if 'analysis' in st.session_state:
    analysis = st.session_state.analysis
    
    st.write("---")
    st.write("## نتایج تحلیل")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("امتیاز کلی", f"{analysis['overall_score']}/10")
        st.info(analysis['summary'])
    
    st.write("---")
    st.markdown('<div class="section-title">🎯 ارزیابی اصول طراحی</div>', unsafe_allow_html=True)
    
    for p in analysis['principles']:
        emoji = {"good": "✅", "needs-work": "⚠️", "poor": "❌"}.get(p['status'], "•")
        status = {"good": "عالی", "needs-work": "نیاز به بهبود", "poor": "ضعیف"}.get(p['status'], "")
        css_class = {"good": "principle-good", "needs-work": "principle-needs-work", "poor": "principle-poor"}.get(p['status'], "")
        
        st.markdown(f"""
        <div class="principle-card {css_class}">
            <h3>{emoji} {p['name']} - امتیاز: {p['score']}/10</h3>
            <p><strong>وضعیت:</strong> {status}</p>
            <p><strong>تحلیل:</strong> {p['feedback']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown('<div class="section-title">💡 پیشنهادهای بهینه‌سازی</div>', unsafe_allow_html=True)
    
    tabs = st.tabs([f"نسخه {i+1}: {opt['focus']}" for i, opt in enumerate(analysis['optimizations'])])
    
    for i, (tab, opt) in enumerate(zip(tabs, analysis['optimizations'])):
        with tab:
            st.write("### 📌 خلاصه")
            st.write(opt['description'])
            st.write("---")
            
            st.write("### 🎨 توصیف بصری")
            st.write(opt['visual_description'])
            st.write("---")
            
            st.write("### 📋 مراحل پیاده‌سازی")
            for idx, step in enumerate(opt.get('implementation_steps', []), 1):
                st.write(f"{idx}. {step}")
            st.write("---")
            
            st.write("### 🔧 تغییرات تفصیلی")
            for j, ch in enumerate(opt['changes'], 1):
                st.markdown(f"""
                <div class="optimization-card">
                    <h4>{j}. {ch['aspect']}</h4>
                    <p><strong>🔍 دلیل:</strong> {ch['reason']}</p>
                    <p><strong>📈 بهبود:</strong> {ch['improvement']}</p>
                    <p><strong>⚙️ راهنما:</strong> {ch.get('specific_instructions', '-')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("تحلیل جدید"):
            del st.session_state.analysis
            st.rerun()
    with col2:
        st.download_button(
            "دانلود گزارش",
            json.dumps(analysis, indent=2, ensure_ascii=False),
            "تحلیل.json"
        )

