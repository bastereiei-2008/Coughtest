import streamlit as st
import time

# --- 1. ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="Smart Cough Screening",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. จัดการ State และตัวแปร ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'symptoms' not in st.session_state: st.session_state.symptoms = []
if 'duration' not in st.session_state: st.session_state.duration = 1

# --- 3. ฟังก์ชัน CSS สำหรับ Theme และ Card UI ---
def inject_custom_css(dark_mode):
    if dark_mode:
        # Dark Mode Theme
        bg_color = "#0E1117"
        card_bg = "#262730"
        text_color = "#FAFAFA"
        secondary_text = "#A3A8B8"
        accent_color = "#4E8CF6"
    else:
        # Light Mode Theme (Professional Medical)
        bg_color = "#F0F2F6"
        card_bg = "#FFFFFF"
        text_color = "#31333F"
        secondary_text = "#656875"
        accent_color = "#007BFF"

    st.markdown(f"""
    <style>
        /* พื้นหลังหลัก */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* สไตล์การ์ด (Card UI) */
        .css-card {{
            border-radius: 15px;
            padding: 30px;
            background-color: {card_bg};
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        /* หัวข้อ */
        h1, h2, h3 {{
            color: {text_color} !important;
            font-family: 'Helvetica Neue', sans-serif;
        }}
        
        /* ปุ่มกด */
        .stButton>button {{
            border-radius: 10px;
            height: 3em;
            font-weight: 600;
            width: 100%;
            border: none;
            transition: all 0.3s;
        }}
        
        /* Custom Highlight Text */
        .highlight {{
            color: {accent_color};
            font-weight: bold;
        }}
        
        /* ซ่อน Footer ของ Streamlit */
        footer {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)

# --- 4. Sidebar (เมนูข้าง) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
    st.title("Smart Cough AI")
    st.caption("v1.0.0 (Prototype)")
    
    st.divider()
    
    # ปุ่มปรับ Dark Mode
    is_dark = st.toggle("🌙 Dark Mode", value=False)
    inject_custom_css(is_dark)
    
    st.divider()
    
    # Progress Bar
    steps = ["Home", "Audio Analysis", "Symptom Check", "Result"]
    current_step = st.session_state.page - 1
    st.write("**Current Step:**")
    st.progress(current_step / (len(steps)-1))
    st.caption(f"Step {st.session_state.page}: {steps[current_step]}")

# --- 5. Mock AI Function ---
def mock_prediction(symptoms):
    # Logic เดิม
    scores = {"RSV": 10, "Whooping Cough": 10, "Pneumonia": 10}
    if "หายใจเสียงหวีด (Wheezing)" in symptoms: scores["RSV"] += 40
    if "มีไข้ต่ำๆ" in symptoms: scores["RSV"] += 20
    if "น้ำมูกไหล/จาม" in symptoms: scores["RSV"] += 20
    if "ไอเป็นชุดยาวๆ หน้าดำหน้าแดง" in symptoms: scores["Whooping Cough"] += 50
    if "หายใจเข้ามีเสียงวู๊บ (Whoop)" in symptoms: scores["Whooping Cough"] += 40
    if "อาเจียนหลังไอ" in symptoms: scores["Whooping Cough"] += 30
    if "เจ็บหน้าอกเวลาหายใจ" in symptoms: scores["Pneumonia"] += 40
    if "หายใจหอบเหนื่อย" in symptoms: scores["Pneumonia"] += 30
    if "มีไข้สูง หนาวสั่น" in symptoms: scores["Pneumonia"] += 30
    if "มีเสมหะสีเขียวหรือคล้ำ" in symptoms: scores["Pneumonia"] += 20

    pred = max(scores, key=scores.get)
    conf = min(scores[pred], 98.5)
    return pred, conf

# --- 6. Navigation Functions ---
def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1
def reset(): 
    st.session_state.page = 1
    st.session_state.symptoms = []
    st.session_state.duration = 1

# ==========================================
# PAGE 1: Welcome & Agreement
# ==========================================
if st.session_state.page == 1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.title("ระบบคัดกรองโรคทางเดินหายใจ")
    st.markdown("### Respiratory Disease Screening System")
    st.write("---")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.info("👋 **สวัสดีครับ** ระบบนี้จะช่วยประเมินความเสี่ยงเบื้องต้นจากเสียงไอและอาการร่วมของคุณ ด้วยเทคโนโลยี AI")
        st.markdown("""
        **โรคที่รองรับการคัดกรอง:**
        * 🦠 **RSV** (ไวรัส RSV)
        * 😷 **Whooping Cough** (โรคไอกรน)
        * 🫁 **Pneumonia** (โรคปอดบวม)
        """)
    
    with c2:
        st.warning("**⚠️ คำเตือน (Disclaimer)**\n\nผลลัพธ์จากระบบนี้เป็นเพียงการวิเคราะห์เบื้องต้น (Prototype) ไม่สามารถใช้แทนคำวินิจฉัยของแพทย์ได้")
        st.write("")
        if st.button("ยอมรับและเริ่มใช้งาน ➔", type="primary"):
            next_page()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: Audio Recording
# ==========================================
elif st.session_state.page == 2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("🎙️ ขั้นตอนที่ 1: วิเคราะห์เสียงไอ")
    st.caption("ระบบ AI จะทำการแยกแยะลักษณะเสียงไอ (Dry/Wet) และรูปแบบความถี่เสียง")
    
    # พื้นที่จำลองกราฟเสียง (เพื่อความสวยงาม)
    st.markdown("---")
    
    # Audio Input
    audio = st.audio_input("กดปุ่มสีแดงเพื่อเริ่มบันทึกเสียง (3-5 วินาที)")
    
    if audio:
        st.success("✅ บันทึกเสียงสำเร็จ! (Audio Quality: High)")
        st.audio(audio)
        st.markdown("---")
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("วิเคราะห์เสียงและทำต่อ ➔", type="primary"):
                next_page()
    else:
        # ปุ่มข้ามสำหรับ Demo
        st.write("")
        if st.button("ข้าม (ใช้เสียงจำลองสำหรับ Demo) ➔"):
            next_page()
            
    st.button("🔙 ย้อนกลับ", on_click=prev_page)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: Symptoms
# ==========================================
elif st.session_state.page == 3:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("📝 ขั้นตอนที่ 2: ประเมินอาการร่วม")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**อาการทั่วไป (General)**")
        s1 = st.checkbox("มีไข้ต่ำๆ")
        s2 = st.checkbox("มีไข้สูง หนาวสั่น")
        s3 = st.checkbox("น้ำมูกไหล / จาม")
        s4 = st.checkbox("เจ็บหน้าอกเวลาหายใจ")
        
    with col2:
        st.markdown("**อาการเกี่ยวกับระบบหายใจ (Respiratory)**")
        s5 = st.checkbox("หายใจเสียงหวีด (Wheezing)")
        s6 = st.checkbox("หายใจเข้ามีเสียงวู๊บ (Whoop)")
        s7 = st.checkbox("หายใจหอบเหนื่อย")
        s8 = st.checkbox("ไอเป็นชุดยาวๆ หน้าดำหน้าแดง")
        s9 = st.checkbox("มีเสมหะสีเขียวหรือคล้ำ")
        s10 = st.checkbox("อาเจียนหลังไอ")

    # รวบรวมอาการ
    current_symptoms = []
    if s1: current_symptoms.append("มีไข้ต่ำๆ")
    if s2: current_symptoms.append("มีไข้สูง หนาวสั่น")
    if s3: current_symptoms.append("น้ำมูกไหล/จาม")
    if s4: current_symptoms.append("เจ็บหน้าอกเวลาหายใจ")
    if s5: current_symptoms.append("หายใจเสียงหวีด (Wheezing)")
    if s6: current_symptoms.append("หายใจเข้ามีเสียงวู๊บ (Whoop)")
    if s7: current_symptoms.append("หายใจหอบเหนื่อย")
    if s8: current_symptoms.append("ไอเป็นชุดยาวๆ หน้าดำหน้าแดง")
    if s9: current_symptoms.append("มีเสมหะสีเขียวหรือคล้ำ")
    if s10: current_symptoms.append("อาเจียนหลังไอ")
    
    st.session_state.symptoms = current_symptoms

    st.write("---")
    st.markdown("**ระยะเวลาที่เป็น (Duration)**")
    st.session_state.duration = st.slider("จำนวนวันที่มีอาการ", 1, 30, 3, format="%d วัน")
    
    c1, c2 = st.columns([1, 1])
    with c1: st.button("🔙 ย้อนกลับ", on_click=prev_page)
    with c2: st.button("ประมวลผลการวินิจฉัย 🔍", on_click=next_page, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 4: Result (Report Style)
# ==========================================
elif st.session_state.page == 4:
    # Animation
    with st.spinner('AI Processing... Analyzing Mel-Spectrogram & Symptoms vector...'):
        time.sleep(1.5)
        
    pred_disease, confidence = mock_prediction(st.session_state.symptoms)
    
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.title("📄 ผลการคัดกรอง (Screening Report)")
    st.caption(f"Date: {time.strftime('%Y-%m-%d')} | AI Model v1.0")
    st.write("---")
    
    # ส่วนแสดงผลลัพธ์หลัก
    col_res1, col_res2 = st.columns([2, 1])
    
    with col_res1:
        st.markdown(f"### ความเสี่ยงสูงที่จะเป็น: <span class='highlight'>{pred_disease}</span>", unsafe_allow_html=True)
        st.write(f"จากการวิเคราะห์เสียงไอและอาการร่วมของคุณในช่วง {st.session_state.duration} วันที่ผ่านมา")
        
        # คำแนะนำ
        st.info("💡 **คำแนะนำเบื้องต้น (Recommendation)**")
        if pred_disease == "RSV":
            st.write("- พักผ่อนให้เพียงพอ ดื่มน้ำสะอาดมากๆ")
            st.write("- หากมีอาการหอบเหนื่อย ควรรีบพบแพทย์")
        elif pred_disease == "Whooping Cough":
            st.write("- ควรแยกตัวจากผู้อื่นเพื่อป้องกันการแพร่เชื้อ")
            st.write("- ควรพบแพทย์เพื่อพิจารณาการรับยาปฏิชีวนะ")
        else: # Pneumonia
            st.error("⚠️ **ข้อควรระวัง:** โรคปอดบวมเป็นภาวะที่ควรได้รับการดูแลจากแพทย์ โปรดไปโรงพยาบาลเพื่อตรวจวินิจฉัยอย่างละเอียด")

    with col_res2:
        st.markdown("**AI Confidence**")
        st.metric(label="", value=f"{confidence}%")
        st.progress(confidence/100)
        st.caption("ความมั่นใจของโมเดล")

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.button("🏠 กลับหน้าหลัก", on_click=reset)
    with c2:
        st.button("🖨️ พิมพ์ผลลัพธ์ (Simulation)", disabled=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
