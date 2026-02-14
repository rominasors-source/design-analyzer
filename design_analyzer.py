import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Page config
st.set_page_config(page_title="تحلیلگر طراحی هوش مصنوعی", page_icon="🎨", layout="wide")

# Custom CSS for RTL and modern Persian UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');

    * {
        direction: rtl;
        text-align: right;
        font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif !important;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }

    /* Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        letter-spacing: -1px;
    }

    .sub-header {
        text-align: center;
        color: #555;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stTextInput input {
        background-color: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white !important;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
    }

    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }

    /* Cards */
    .css-1r6slb0 {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }

    /* Expander - HIDE THE KEY TEXT */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    /* Hide the key parameter in expanders */
    .streamlit-expanderHeader p {
        font-family: 'Vazirmatn', sans-serif !important;
    }

    .streamlit-expanderHeader [data-testid="stMarkdownContainer"] p:last-child {
        display: none !important;
    }

    .streamlit-expanderContent {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
        padding: 1.5rem;
        background: white;
        border-radius: 0 0 10px 10px;
    }

    .streamlit-expanderContent * {
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* Principle container */
    .principle-good {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-right: 5px solid #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    .principle-needs-work {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-right: 5px solid #ffc107;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    .principle-poor {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-right: 5px solid #dc3545;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Info boxes */
    .stAlert {
        background: white;
        border-radius: 12px;
        border-right: 5px solid #667eea;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        border: 3px dashed #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    /* Checkboxes */
    .stCheckbox {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .stCheckbox:hover {
        background: #f8f9fa;
        transform: translateX(-3px);
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #2d3748;
        font-weight: 700;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    h2 {
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(72, 198, 239, 0.4);
        width: 100%;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(72, 198, 239, 0.6);
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Caption */
    .css-1v0mbdj {
        color: #718096;
        font-size: 0.95rem;
    }

    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border-radius: 12px;
        padding: 1rem;
        border-right: 5px solid #28a745;
    }

    /* Error message */
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        border-radius: 12px;
        padding: 1rem;
        border-right: 5px solid #dc3545;
    }

    /* Fix for all markdown content */
    .stMarkdown {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stMarkdown * {
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* Fix for paragraphs */
    p, span, div {
        font-family: 'Vazirmatn', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎨 تحلیلگر طراحی با هوش مصنوعی</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">لوگوی خود را آپلود کنید و تحلیل حرفه‌ای دریافت کنید</p>', unsafe_allow_html=True)

# Sidebar for API keys
with st.sidebar:
    st.markdown("### ⚙️ تنظیمات")

    st.markdown("""
    #### 🔑 کلید API گوگل جمینای

    **مراحل دریافت:**
    1. به سایت مراجعه کنید
    2. با حساب گوگل وارد شوید
    3. کلید جدید بسازید
    4. در زیر وارد کنید
    """)

    gemini_api_key = st.text_input("کلید API را وارد کنید", type="password", key="gemini",
                                   placeholder="کلید خود را اینجا وارد کنید...")

    st.markdown("---")

    st.markdown("""
    #### 📚 اصول طراحی

    این ابزار موارد زیر را بررسی می‌کند:

    ✓ تعادل و ترکیب‌بندی  
    ✓ تئوری رنگ و هارمونی  
    ✓ تایپوگرافی حرفه‌ای  
    ✓ کنتراست و خوانایی  
    ✓ مقیاس‌پذیری  
    ✓ سلسله‌مراتب بصری  
    ✓ سادگی و وضوح  
    ✓ حرفه‌ای بودن کلی  
    """)

# Main content
if not gemini_api_key:
    st.info("👈 لطفاً ابتدا کلید API خود را در نوار کناری وارد کنید")
    st.stop()

# Initialize Gemini
try:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("❌ کلید API نامعتبر است. لطفاً دوباره بررسی کنید")
    st.stop()

# File uploader
uploaded_file = st.file_uploader(
    "📤 فایل لوگوی خود را اینجا بکشید یا کلیک کنید",
    type=["png", "jpg", "jpeg", "webp"],
    help="فرمت‌های پشتیبانی شده: PNG, JPG, JPEG, WEBP"
)

if uploaded_file:
    # Display uploaded image
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📤 طراحی شما")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        st.caption(f"📏 اندازه: {image.size[0]} × {image.size[1]} پیکسل  |  📁 فرمت: {image.format}")

    with col2:
        st.markdown("### 🎯 تمرکز بهینه‌سازی")
        st.markdown("جنبه‌هایی که می‌خواهید بهبود یابند را انتخاب کنید:")

        focus_minimalism = st.checkbox("🎨 مینیمالیسم و سادگی", value=False)
        focus_accessibility = st.checkbox("♿ دسترسی‌پذیری و خوانایی", value=False)
        focus_modern = st.checkbox("✨ ترندهای مدرن", value=False)
        focus_color = st.checkbox("🌈 هارمونی رنگی", value=False)
        focus_scalability = st.checkbox("📐 مقیاس‌پذیری", value=False)

    # Build focus string
    focus_areas = []
    if focus_minimalism:
        focus_areas.append("مینیمالیسم و سادگی")
    if focus_accessibility:
        focus_areas.append("دسترسی‌پذیری و خوانایی")
    if focus_modern:
        focus_areas.append("ترندهای مدرن طراحی")
    if focus_color:
        focus_areas.append("هارمونی رنگی و بهینه‌سازی پالت")
    if focus_scalability:
        focus_areas.append("مقیاس‌پذیری در اندازه‌ها و زمینه‌های مختلف")

    focus_instruction = ""
    if focus_areas:
        focus_instruction = f"\n\nطراح به طور خاص می‌خواهد برای موارد زیر بهینه‌سازی انجام شود: {', '.join(focus_areas)}. لطفاً این جنبه‌ها را در پیشنهادات بهینه‌سازی در اولویت قرار دهید."

    st.markdown("---")

    # Analyze button
    if st.button("🚀 شروع تحلیل هوشمند", type="primary"):
        with st.spinner("🤖 هوش مصنوعی در حال بررسی دقیق طراحی شماست..."):
            try:
                # Reset image pointer
                uploaded_file.seek(0)
                image = Image.open(uploaded_file)

                # Create prompt for Gemini in Farsi
                prompt = f"""شما یک منتقد و مشاور طراحی خبره هستید. این طراحی لوگو را بر اساس اصول اساسی طراحی تحلیل کنید.

تحلیل خود را به فرمت JSON زیر ارائه دهید (تمام متن‌ها باید به فارسی باشند):

{{
    "overall_score": <عدد از 1 تا 10>,
    "summary": "<ارزیابی کلی مختصر به فارسی>",
    "principles": [
        {{
            "name": "<نام اصل به فارسی>",
            "status": "<good/needs-work/poor>",
            "score": <عدد از 1 تا 10>,
            "feedback": "<بازخورد تفصیلی به فارسی>"
        }}
    ],
    "optimizations": [
        {{
            "version": "<شماره/نام نسخه به فارسی>",
            "focus": "<این بهینه‌سازی روی چه چیزی تمرکز دارد - به فارسی>",
            "visual_description": "<توصیف بصری بسیار دقیق لوگوی بهینه‌شده - رنگ‌های دقیق، اشکال، انتخاب‌های تایپوگرافی، چیدمان، فاصله‌گذاری، روابط اندازه، سبک را شرح دهید - به فارسی>",
            "implementation_steps": [
                "<مرحله 1 به فارسی>",
                "<مرحله 2 به فارسی>",
                "<مرحله 3 به فارسی>"
            ],
            "changes": [
                {{
                    "aspect": "<چه چیزی تغییر کرد - به فارسی>",
                    "reason": "<چرا تغییر کرد - به فارسی>",
                    "improvement": "<بهبود مورد انتظار - به فارسی>",
                    "specific_instructions": "<مشخصات دقیق برای پیاده‌سازی این تغییر - به فارسی>"
                }}
            ],
            "description": "<توضیح متنی نسخه بهینه‌شده - به فارسی>"
        }}
    ]
}}

این اصول طراحی را تحلیل کنید:
1. تعادل و ترکیب‌بندی
2. تئوری رنگ و هارمونی
3. تایپوگرافی (اگر متن وجود دارد)
4. کنتراست و خوانایی
5. مقیاس‌پذیری
6. سلسله‌مراتب بصری
7. سادگی و وضوح
8. حرفه‌ای بودن

3 پیشنهاد بهینه‌سازی مختلف با توضیحات بسیار دقیق ارائه دهید.

مهم: برای هر بهینه‌سازی:
- یک توصیف بصری بسیار دقیق ارائه دهید که یک طراح بتواند از آن برای بازسازی لوگو استفاده کند
- کدهای رنگی مشخص، پیشنهادات فونت، اندازه‌گیری‌های فاصله‌گذاری را شامل شود
- دستورالعمل‌های پیاده‌سازی مرحله به مرحله ارائه دهید
- در مورد هر عنصر بصری تا حد امکان دقیق باشید{focus_instruction}

تمام پاسخ‌ها باید به زبان فارسی باشند.
فقط JSON معتبر برگردانید، بدون هیچ متن یا قالب‌بندی مارک‌داون دیگری."""

                # Call Gemini API
                response = model.generate_content([prompt, image])
                response_text = response.text

                # Try to extract JSON if there's any surrounding text
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()

                # Remove any leading/trailing whitespace
                response_text = response_text.strip()

                analysis = json.loads(response_text)

                # Store in session state
                st.session_state.analysis = analysis
                st.session_state.original_image = image

            except json.JSONDecodeError as e:
                st.error("❌ خطا در دریافت پاسخ. لطفاً دوباره تلاش کنید")
                with st.expander("🔍 مشاهده جزئیات خطا"):
                    st.code(response_text)
                st.stop()
            except Exception as e:
                st.error(f"❌ خطا: {str(e)}")
                st.stop()

        st.success("✅ تحلیل با موفقیت انجام شد!")
        st.rerun()

# Display results if available
if 'analysis' in st.session_state:
    analysis = st.session_state.analysis

    st.markdown("---")
    st.markdown("## 📊 نتایج تحلیل")

    # Overall score
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("امتیاز کلی طراحی", f"{analysis['overall_score']}/10", delta=None)
        st.info(f"💬 {analysis['summary']}")

    st.markdown("---")

    # Design principles breakdown
    st.markdown("## 🎯 ارزیابی اصول طراحی")

    for idx, principle in enumerate(analysis['principles']):
        status_class = principle['status']
        emoji_map = {
            "good": "✅",
            "needs-work": "⚠️",
            "poor": "❌"
        }

        status_farsi = {
            "good": "عالی",
            "needs-work": "نیاز به بهبود",
            "poor": "ضعیف"
        }

        # Use index as key to avoid the key parameter showing
        expander_label = f"{emoji_map.get(status_class, '•')} {principle['name']} — امتیاز: {principle['score']}/10"

        with st.expander(expander_label, expanded=False):
            st.markdown(f"**🏷️ وضعیت:** {status_farsi.get(status_class, status_class)}")
            st.markdown(f"**📝 تحلیل:** {principle['feedback']}")

    st.markdown("---")

    # Optimization suggestions
    st.markdown("## 💡 پیشنهادهای بهینه‌سازی")
    st.info("📋 در زیر سه نسخه بهینه‌شده با جزئیات کامل آمده است")

    for i, opt in enumerate(analysis['optimizations'], 1):
        expander_title = f"🎨 نسخه {i}: {opt['focus']}"

        with st.expander(expander_title, expanded=(i == 1)):
            st.markdown(f"### 📌 خلاصه")
            st.markdown(f"*{opt['description']}*")

            st.markdown("---")

            st.markdown("### 🎨 توصیف بصری کامل")
            st.markdown(opt['visual_description'])

            st.markdown("---")

            st.markdown("### 📋 مراحل پیاده‌سازی")
            for idx, step in enumerate(opt.get('implementation_steps', []), 1):
                st.markdown(f"**{idx}.** {step}")

            st.markdown("---")

            st.markdown("### 🔧 تغییرات تفصیلی")
            for j, change in enumerate(opt['changes'], 1):
                st.markdown(f"#### {j}. {change['aspect']}")
                st.markdown(f"**🔍 دلیل تغییر:** {change['reason']}")
                st.markdown(f"**📈 بهبود مورد انتظار:** {change['improvement']}")
                st.markdown(
                    f"**⚙️ راهنمای پیاده‌سازی:** {change.get('specific_instructions', 'به توصیف بصری بالا مراجعه کنید')}")

                if j < len(opt['changes']):
                    st.markdown("---")

    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🔄 تحلیل لوگوی جدید", type="secondary"):
            if 'analysis' in st.session_state:
                del st.session_state.analysis
            if 'original_image' in st.session_state:
                del st.session_state.original_image
            st.rerun()

    with col2:
        # Download analysis as JSON
        analysis_json = json.dumps(analysis, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 دانلود گزارش کامل",
            data=analysis_json,
            file_name="تحلیل_طراحی.json",
            mime="application/json"
        )

