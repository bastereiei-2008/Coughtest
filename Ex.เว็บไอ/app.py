import streamlit as st
import time

# --- 1. ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="Smart Cough Screening",
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
    st.title("Smart Cough AI")
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
    st.markdown("### ระบบคัดกรองโรคทางเดินหายใจในเด็กเบื้องต้น\n\ระบบคัดกรองโรคทาเดินหายใจในเด็กแรกเกิดถึงเด็กอายุ5ปี")
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
        if st.button("ยอมรับเงื่อนไขและเริ่มต้นใช้งาน ➔", type="primary"):
            next_page()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: Audio Recording
# ==========================================
elif st.session_state.page == 2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("🎙️ ขั้นตอนที่ 1: วิเคราะห์เสียงไอ (Cough Analysis)")
    st.caption("กรุณากดปุ่มสีแดงเพื่อบันทึกเสียงไอของผู้ป่วย (ระยะเวลา 3-5 วินาที)")
    st.write("") 
    
    c_left, c_center, c_right = st.columns([1, 2, 1])
    
    with c_center:
        st.markdown("⬇️ **แตะที่นี่เพื่อเริ่มบันทึกเสียง** ⬇️")
        audio = st.audio_input("Record") 
    
    if audio:
        st.write("")
        st.success("✅ บันทึกเสียงสำเร็จ (Audio Quality: High)")
        st.audio(audio)
        st.markdown("---")
        
        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            if st.button("วิเคราะห์เสียงและดำเนินการต่อ ➔", type="primary"):
                next_page()
    else:
        st.info("💡 กรุณากดปุ่มไมโครโฟนเพื่อบันทึกเสียง")
            
    st.write("")
    st.button("🔙 ย้อนกลับ", on_click=prev_page)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: Symptoms Check
# ==========================================
elif st.session_state.page == 3:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("📝 ขั้นตอนที่ 2: ประเมินอาการร่วม (Symptoms Assessment)")
    st.write("กรุณาเลือกอาการที่ปรากฏในปัจจุบัน (Select all that apply)")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        s1 = st.checkbox("มีไข้ต่ำๆ (Low-grade fever)")
        s2 = st.checkbox("มีไข้สูง หนาวสั่น (High fever & Chills)")
        s3 = st.checkbox("น้ำมูกไหล / จาม (Runny nose)")
        
    with col2:
        s4 = st.checkbox("เจ็บหน้าอกเวลาหายใจ (Chest pain)")
        s5 = st.checkbox("มีเสมหะสีเขียวหรือคล้ำ (Phlegm)")
        s6 = st.checkbox("อาเจียนหลังไอ (Post-tussive vomiting)")

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
    st.markdown("**ระยะเวลาที่มีอาการ (Duration of Symptoms)**")
    st.session_state.duration = st.slider("จำนวนวัน (Days)", 1, 30, 3)
    
    c1, c2 = st.columns([1, 1])
    with c1: st.button("🔙 ย้อนกลับ", on_click=prev_page)
    with c2: st.button("ประมวลผลการวินิจฉัย 🔍", on_click=next_page, type="primary")
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
            st.error("⚠️ **ข้อควรระวัง:** โรคปอดบวมเป็นภาวะที่ควรได้รับการดูแลจากแพทย์ โปรดเข้ารับการตรวจวินิจฉัยอย่างละเอียดที่โรงพยาบาล")

    with col_res2:
        st.markdown("**AI Confidence Score**")
        st.metric(label="", value=f"{confidence}%")
        st.progress(confidence/100)
        st.caption("ระดับความเชื่อมั่นของโมเดล")

    st.write("---")
    c1, c2 = st.columns(2)
    with c1: st.button("🏠 กลับหน้าหลัก", on_click=reset)
    with c2: st.button("🖨️ พิมพ์ผลลัพธ์ (Simulation)", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

