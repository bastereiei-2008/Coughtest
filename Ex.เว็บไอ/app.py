import streamlit as st
import time

# --- 1. ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="CoughCareKids",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. State Management ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'symptoms' not in st.session_state: st.session_state.symptoms = []
if 'duration' not in st.session_state: st.session_state.duration = 1

# --- 3. CSS (Theme: Clean White / Medical Professional) ---
def inject_custom_css():
    # โทนสีขาว-ฟ้า-เทา ให้ความรู้สึกสะอาดและน่าเชื่อถือ
    bg_color = "#F0F2F6"
    card_bg = "#FFFFFF"
    text_color = "#31333F"
    mic_bg = "rgba(255, 75, 75, 0.05)"
    accent_color = "#007BFF"

    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        
        /* Card UI แบบเรียบหรู */
        .css-card {{
            border-radius: 12px;
            padding: 30px;
            background-color: {card_bg};
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid #E6E9EF;
        }}
        
        /* ปุ่มกด Standard Medical Style */
        .stButton>button {{
            border-radius: 8px;
            height: 3em;
            font-weight: 500;
            width: 100%;
            border: none;
            transition: all 0.2s;
        }}
        
        /* Highlight โซนอัดเสียงให้เด่นแต่สุภาพ */
        div[data-testid="stAudioInput"] {{
            border: 2px solid #FF4B4B !important;
            background-color: {mic_bg} !important;
            border-radius: 15px !important;
            padding: 40px !important;
            text-align: center !important;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.1);
        }}
        
        /* Typography */
        h1, h2, h3 {{
            font-family: 'Helvetica Neue', 'Sarabun', sans-serif;
            color: #2C3E50 !important;
        }}
        
        .highlight {{ color: {accent_color}; font-weight: bold; }}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- 4. Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
    st.title("CoughCareKids")
    st.caption("v1.0.4 (Professional)")
    st.divider()
    
    # Progress Bar
    steps = ["Home", "Audio Analysis", "Symptom Check", "Result"]
    current_step = st.session_state.page - 1
    st.write("**Current Step:**")
    st.progress(current_step / (len(steps)-1))
    st.caption(f"Status: {steps[current_step]}")

# --- 5. Mock AI Logic (Logic เดิมที่ตัดเสียงไอออกจาก Checkbox) ---
def mock_prediction(symptoms):
    scores = {"RSV": 10, "Whooping Cough": 10, "Pneumonia": 10}
    
    # Logic การวิเคราะห์จากอาการที่เหลืออยู่
    if "มีไข้ต่ำๆ" in symptoms: scores["RSV"] += 40
    if "น้ำมูกไหล / จาม" in symptoms: scores["RSV"] += 40
    
    if "อาเจียนหลังไอ" in symptoms: scores["Whooping Cough"] += 60
    if "มีไข้สูง หนาวสั่น" not in symptoms: scores["Whooping Cough"] += 20 

    if "เจ็บหน้าอกเวลาหายใจ" in symptoms: scores["Pneumonia"] += 40
    if "มีไข้สูง หนาวสั่น" in symptoms: scores["Pneumonia"] += 30
    if "มีเสมหะสีเขียวหรือคล้ำ" in symptoms: scores["Pneumonia"] += 30

    pred = max(scores, key=scores.get)
    conf = min(scores[pred], 98.5)
    return pred, conf

# --- 6. Navigation ---
def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1
def reset(): 
    st.session_state.page = 1
    st.session_state.symptoms = []
    st.session_state.duration = 1

# ==========================================
# PAGE 1: Welcome
# ==========================================
if st.session_state.page == 1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.title("Cough Care Kids")
    st.markdown("### ระบบคัดกรองโรคทางเดินหายใจในเด็กเบื้องต้น\nระบบคัดกรองโรคทาเดินหายใจในเด็กแรกเกิดถึงเด็กอายุ5ปี")
    st.write("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.info("👋 **สวัสดีครับ** ระบบนี้จะช่วยประเมินความน่าจะเป็นของโรคเบื้องต้นจากเสียงไอและอาการร่วมของคุณ ด้วยเทคโนโลยี AI")
        st.markdown("""
        **ขอบเขตการคัดกรอง (Scope of Screening):**
        * 🦠 **RSV** (Respiratory Syncytial Virus)
        * 😷 **Whooping Cough** (โรคไอกรน)
        * 🫁 **Pneumonia** (โรคปอดอักเสบหรือปอดบวม)
        """)
    with c2:
        st.warning("**⚠️ คำเตือน**\n\nผลลัพธ์นี้เป็นเพียงการวิเคราะห์เบื้องต้นจากปัญญาประดิษฐ์ ไม่สามารถใช้แทนการวินิจฉัยของแพทย์ได้")
        st.write("")
        if st.button("ยอมรับเงื่อนไขและเริ่มต้นใช้งาน", type="primary"):
            next_page()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: Audio Recording (Pure Mic Button)
# ==========================================
elif st.session_state.page == 2:
    # --- CSS: ซ่อนทุกอย่างยกเว้นปุ่มไมค์ ---
    st.markdown("""
    <style>
        /* 1. จัดตำแหน่งปุ่มให้อยู่กึ่งกลาง */
        div[data-testid="stAudioInput"] {
            margin: auto !important;
            width: fit-content !important;
        }

        /* 2. ปรับปุ่มกด (Start/Stop) ให้เป็นวงกลมแดงใหญ่ */
        div[data-testid="stAudioInput"] > button:first-child {
            background-color: #FF4B4B !important;
            width: 180px !important;
            height: 180px !important;
            border-radius: 50% !important;
            border: 5px solid #FFEBEE !important;
            box-shadow: 0 4px 20px rgba(255, 75, 75, 0.3) !important;
        }
        
        /* เอฟเฟกต์ตอนชี้ */
        div[data-testid="stAudioInput"] > button:first-child:hover {
            transform: scale(1.05);
            background-color: #D32F2F !important;
        }

        /* 3. ขยายไอคอนไมค์ข้างใน */
        div[data-testid="stAudioInput"] > button:first-child svg {
            width: 70px !important;
            height: 70px !important;
            fill: white !important;
        }

        /* --- 4. สำคัญ: ซ่อนปุ่มถังขยะ (Delete) --- */
        div[data-testid="stAudioInput"] button[aria-label="Clear"],
        div[data-testid="stAudioInput"] button[kind="secondary"] {
            display: none !important;
        }

        /* --- 5. ซ่อนปุ่ม Download (ถ้ามี) และ Waveform --- */
        /* ซ่อนเครื่องเล่นเสียงตัวเต็ม เพื่อไม่ให้มีปุ่ม Save/Download */
        div[data-testid="stAudioInput"] audio {
            display: none !important; 
        }
        
        /* ซ่อน Canvas (คลื่นเสียง) */
        div[data-testid="stAudioInput"] canvas {
            display: none !important;
        }

        /* ซ่อนข้อความ Label */
        div[data-testid="stAudioInput"] label { display: none !important; }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("🎙️วิเคราะห์เสียงไอ")
    
    st.markdown(
        "<h3 style='text-align: center; color: #555;'>กดปุ่มเพื่อเริ่ม/หยุด</h3>", 
        unsafe_allow_html=True
    )
    st.write("") 
    
    # --- ปุ่มอัดเสียง ---
    audio = st.audio_input("Record") 
    
    # --- Logic ---
    if audio:
        # เมื่อได้ไฟล์เสียงแล้ว (กดหยุดแล้ว)
        st.write("")
        
        # แสดงสถานะว่าได้รับเสียงแล้ว (แทนเครื่องเล่นเสียงที่ถูกซ่อนไป)
        st.markdown("""
            <div style="
                background-color: #E8F5E9; 
                padding: 15px; 
                border-radius: 50px; 
                text-align: center; 
                color: #2E7D32; 
                font-weight: bold; 
                border: 2px solid #A5D6A7;
                width: fit-content;
                margin: 0 auto;">
                ✅ ได้รับเสียงเรียบร้อย
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        # ปุ่มไปต่อ
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("ถัดไป", type="primary"):
                next_page()
    else:
        # พื้นที่ว่าง
        st.write("<br><br>", unsafe_allow_html=True)

    st.write("")
    if st.button("ย้อนกลับ", key="back_btn"):
        prev_page()
        
    st.markdown('</div>', unsafe_allow_html=True)
# ==========================================
# PAGE 3: Symptoms Check
# ==========================================
elif st.session_state.page == 3:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("ประเมินอาการร่วมด้วย")
    st.write("กรุณาเลือกอาการร่วมด้วยและระยะเวลา")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        s1 = st.checkbox("มีไข้ต่ำๆ")
        s2 = st.checkbox("มีไข้สูง หนาวสั่น")
        s3 = st.checkbox("น้ำมูกไหล / จาม")
        
    with col2:
        s4 = st.checkbox("เจ็บหน้าอกเวลาหายใจ")
        s5 = st.checkbox("มีเสมหะสีเขียวหรือคล้ำ")
        s6 = st.checkbox("อาเจียนหลังไอ")

    # รวบรวมอาการ
    current_symptoms = []
    if s1: current_symptoms.append("มีไข้ต่ำๆ")
    if s2: current_symptoms.append("มีไข้สูง หนาวสั่น")
    if s3: current_symptoms.append("น้ำมูกไหล / จาม")
    if s4: current_symptoms.append("เจ็บหน้าอกเวลาหายใจ")
    if s5: current_symptoms.append("มีเสมหะสีเขียวหรือคล้ำ")
    if s6: current_symptoms.append("อาเจียนหลังไอ")
    
    st.session_state.symptoms = current_symptoms

    st.write("---")
    st.markdown("**ระยะเวลาที่มีอาการ**")
    st.session_state.duration = st.slider("จำนวนวัน (Days)", 1, 30, 3)
    
    c1, c2 = st.columns([1, 1])
    with c1: st.button("ย้อนกลับ", on_click=prev_page)
    with c2: st.button("วิเคราะห์", on_click=next_page, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 4: Screening Report
# ==========================================
elif st.session_state.page == 4:
    with st.spinner('AI Processing... Analyzing Mel-Spectrogram & Clinical Data...'):
        time.sleep(1.5)
    pred_disease, confidence = mock_prediction(st.session_state.symptoms)
    
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.title("📄 ผลการคัดกรอง (Screening Report)")
    st.caption(f"Date: {time.strftime('%Y-%m-%d')} | AI Model v1.0")
    st.write("---")
    
    col_res1, col_res2 = st.columns([2, 1])
    with col_res1:
        st.markdown(f"### ความเสี่ยงสูงที่จะเป็น: <span class='highlight'>{pred_disease}</span>", unsafe_allow_html=True)
        st.write(f"จากการวิเคราะห์เสียงไอและประวัติอาการในช่วง {st.session_state.duration} วันที่ผ่านมา")
        
        st.info("💡 **คำแนะนำเบื้องต้น (Recommendation)**")
        if pred_disease == "RSV":
            st.write("- ควรพักผ่อนให้เพียงพอ และดื่มน้ำสะอาดในปริมาณมาก")
            st.write("- เฝ้าระวังอาการหอบเหนื่อย หากมีอาการควรรีบพบแพทย์ทันที")
        elif pred_disease == "Whooping Cough":
            st.write("- โรคนี้สามารถแพร่กระจายเชื้อได้ง่าย ควรแยกผู้ป่วยจากผู้อื่น")
            st.write("- ควรปรึกษาแพทย์เพื่อพิจารณาการใช้ยาปฏิชีวนะ")
        else: 
            st.error("⚠️ **ข้อควรระวัง:** ผลลัพธ์นี้เป็นเพียงการวิเคราะห์เบื้องต้นจากปัญญาประดิษฐ์ ไม่สามารถใช้แทนการวินิจฉัยของแพทย์ได้")

    with col_res2:
        st.markdown("**AI Confidence Score**")
        st.metric(label="", value=f"{confidence}%")
        st.progress(confidence/100)
        st.caption("ระดับความเชื่อมั่นของโมเดล")

    st.write("---")
    c1, c2 = st.columns(2)
    with c1: st.button("กลับหน้าหลัก", on_click=reset)
    st.markdown('</div>', unsafe_allow_html=True)












