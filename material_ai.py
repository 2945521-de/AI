import streamlit as st
import pandas as pd

# 🔐 비밀번호 설정
PASSWORD = "simwoo"   # 👉 여기 바꾸면 됨

# 🔐 로그인 상태 저장
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 🔐 로그인 화면
if not st.session_state.authenticated:
    st.title("🔒 사내 전용 시스템")
    st.write("비밀번호를 입력하세요")

    pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다")

    st.stop()  # 🔥 여기서 아래 코드 실행 막음

st.set_page_config(layout="centered", page_title="공종별 작업 메뉴얼", page_icon="🏗️")

# =========================
# 세션 상태 초기화
# =========================
if "video_menu" not in st.session_state:
    st.session_state.video_menu = None

if "defect_type" not in st.session_state:
    st.session_state.defect_type = None

if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

if "doc_menu" not in st.session_state:
    st.session_state.doc_menu = None

# =========================
# 전체 스타일 (사이드바 흰색 버튼 복구 포함)
# =========================
st.markdown("""
<style>

/* 기존 스타일 코드들 시작 */
.stApp {
    background-color: #f8f9fa;
}

/* 💻 PC 웹 화면 설정 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 700px !important; 
    margin: 0 auto;
}

/* 🟧 메인 화면 버튼 디자인 (주황색) */
div.stButton > button {
    height: 55px;
    border-radius: 12px;
    background: linear-gradient(135deg, #ffa94d, #ff922b) !important;
    color: white !important;
    font-size: 18px;
    font-weight: 800;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}

/* ⬜ 사이드바 전용 버튼 디자인 (흰색으로 예외 처리) */
section[data-testid="stSidebar"] div.stButton > button {
    background: #ffffff !important;
    color: #212529 !important;
    border: 1px solid #e9ecef !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
    height: auto !important; 
    padding: 12px !important;
    font-size: 15px !important;
    margin-bottom: 10px !important;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #f8f9fa !important;
    transform: translateY(0px) !important; /* 마우스 올렸을 때 위로 들썩임 방지 */
    border-color: #dee2e6 !important;
}

.warning-banner {
    width: 100%;
    text-align: center;
    color: #856404;
    background-color: #fff3cd;
    padding: 12px;
    border-radius: 10px;
    margin-top: 15px;
    font-weight: 600;
    font-size: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.material-wrapper {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
    margin-top: 10px;
}

.material-card {
    background: linear-gradient(135deg, #ffffff, #f1f3f5);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    word-break: keep-all;
    line-height: 1.4;
}

/* 📱 모바일 화면 설정 */
@media screen and (max-width: 768px) {
    .block-container {
        padding-top: 1rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important;
        overflow-x: hidden !important; 
    }
    
    h1 { 
        font-size: 24px !important; 
        white-space: nowrap !important; 
        letter-spacing: -1px !important; 
    }
    h3 { 
        font-size: 16px !important; 
        white-space: nowrap !important; 
        letter-spacing: -1px !important; 
    }
    .sub-title { font-size: 18px !important; }
    
    /* 공종 버튼 3열 강제 고정 */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important; 
        flex-wrap: nowrap !important;
        gap: 5px !important; 
        margin-bottom: 0px !important; 
    }
    
    div[data-testid="column"], div[data-testid="stColumn"] {
        width: 33.33% !important;
        flex: 1 1 33.33% !important; 
        min-width: 0 !important;
        padding: 0 !important; 
    }
    
    /* 모바일용 메인 버튼 크기 최적화 */
    div.stButton > button {
        font-size: 13px !important; 
        letter-spacing: -0.5px !important; 
        height: 42px !important; 
        padding: 0 !important;
        margin: 2px 0px !important; 
    }
    
    /* 모바일에서 사이드바 메뉴 열었을 때 버튼이 찌그러지지 않게 방어 */
    section[data-testid="stSidebar"] div.stButton > button {
        height: auto !important;
        padding: 12px !important;
        font-size: 15px !important;
        margin-bottom: 8px !important;
    }
    
    .material-wrapper {
        grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
        gap: 8px;
    }
    
    .material-card { padding: 8px; font-size: 12px; }
}
</style>
""", unsafe_allow_html=True)


# =========================
# 상단 헤더 및 카테고리
# =========================
# (모바일 최적화를 위해 컬럼을 나누지 않고 컨테이너 너비를 모두 사용합니다)
col_img, col_empty = st.columns([1, 4])
with col_img:
    st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
    st.image("lynn.png", width=80)

# 1. 메인 타이틀 (위치 고정값 제거, 반응형 중앙정렬)
st.markdown("""
<div style="text-align:center; margin-bottom: 20px;">
    <h1 style="margin:0; font-size: 28px;">전유부 공종별 작업 메뉴얼</h1>
    <p class="sub-title" style="font-size:22px; font-weight:700; color:#e67e22; margin-top:10px; margin-bottom:0;">※ 현장별 자재 현황 ※</p>
</div>
""", unsafe_allow_html=True)


# 현장별 자재 현황 선택 UI
site_list = ["현장을 선택하세요", "음성성본1차"]

selected_site = st.selectbox(
    "현장 선택", 
    site_list, 
    index=1, 
    label_visibility="collapsed", 
    key="site_select"
)

# [음성성본1차] 선택 시 엑셀 표시 로직
if selected_site == "음성성본1차":
    excel_files = {
        "자재명": None,
        "타일 자재현황": "(음성성본1차)_하자보수자재(타일).xlsx",
        "도배 자재현황": "(음성성본1차)_하자보수자재(도배).xlsx",
        "마루 자재현황": "(음성성본1차)_하자보수자재(마루).xlsx"
    }
    
    selected_excel = st.selectbox("엑셀 파일 선택", list(excel_files.keys()), label_visibility="collapsed", key="excel_select")
    
    if selected_excel != "자재명":
        file_name = excel_files[selected_excel]
        file_path = f"docs/{file_name}"
        
        try:
            df = pd.read_excel(file_path, header=1)
            df = df.loc[:, ~df.columns.str.contains('Unnamed')]
            df = df.dropna(how='all')
            df = df.fillna("")
            df = df.astype(str).replace(r'\.0$', '', regex=True)

            st.markdown(f"#### 📊 {selected_excel} 현황 데이터")
            st.dataframe(df, use_container_width=True, height=350) # 모바일을 위해 높이 소폭 조정
            
        except FileNotFoundError:
            st.error(f"⚠️ '{file_name}' 파일을 'docs' 폴더 내에서 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"⚠️ 에러 발생: {e}")

# 2. 공종 선택 타이틀
st.markdown("""
<div style="text-align:center; margin-top: 30px; margin-bottom: 15px;">
    <p class="sub-title" style="font-size:24px; font-weight:700; margin:0;">※ 공종 선택 ※</p>
</div>
""", unsafe_allow_html=True)


# =========================
# 공종 버튼 (PC/모바일 모두 3열 유지 + 반응형)
# =========================
types = [
    "타일공사", "방수공사", "미장공사", "도장공사",
    "내장공사", "도배공사", "마루공사", "가구공사",
    "창호공사", "금속공사", "전기공사", "설비공사"
]

for i in range(0, len(types), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(types):
            with cols[j]:
                # 🔥 핵심: use_container_width=True 를 추가하여 버튼이 열(Column) 너비에 꽉 차게 만듭니다.
                if st.button(types[i + j], key=f"type_{i+j}", use_container_width=True):
                    st.session_state.defect_type = types[i + j]
                    st.session_state.search_clicked = False
                    st.session_state.video_menu = None
                    st.session_state.doc_menu = None

if st.session_state.defect_type:
    st.markdown(f"""
    <div style="text-align:center; margin-top:15px; margin-bottom:10px;">
        <p style='font-size:18px; font-weight:600;'>
            선택 공종 : <span style='color:#ff922b'>{st.session_state.defect_type}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 사이드바
# =========================
with st.sidebar:
    st.markdown("### ⚙️ 설정")

    def reset_all():
        st.session_state.defect_type = None
        st.session_state.search_clicked = False
        st.session_state.video_menu = None
        st.session_state.doc_menu = None
        st.session_state.site_select = "음성성본1차"
        st.session_state.excel_select = "자재명"

    st.button("🔄 전체 초기화", on_click=reset_all)

    st.markdown("### 🎬 영상 자료")

    if st.button("안전교육", key="v1"):
        st.session_state.video_menu = "안전교육"

    if st.button("친절교육", key="v2"):
        st.session_state.video_menu = "친절교육"

    if st.button("스마트린", key="v3"):
        st.session_state.video_menu = "스마트린"

    st.divider()

    video_map = {
        "안전교육": [
            ("나를 지키려면", "https://www.youtube.com/watch?v=Z3tuNj82faY&t=131s"),
            ("3대 기초 안전수", "https://www.youtube.com/watch?v=pX3o9lwOoFY"),
            ("추락 재해", "https://www.youtube.com/watch?v=qFpfVIc0j3M"),
            ("안전사고 예방 캠페인", "https://www.youtube.com/watch?v=Ed3S2nY9A7I"),
        ],
        "친절교육": [
            ("세대 하자보수 프로세스", "https://www.youtube.com/watch?v=8JHLXeDPuzs"),
            ("하자보수 계획 통보", "https://www.youtube.com/watch?v=wXrvCgA8D0A"),
            ("개인정보보호", "https://www.youtube.com/watch?v=ZywqqFtJArQ"),
        ],
        "스마트린": [
            ("작업지시서 사용방법", "https://www.youtube.com/watch?v=lYbQjN7Jg5w"),
            ("모바일 AS 접수 이용방법", "https://www.youtube.com/watch?v=CfN0zjOZiC8"),
        ],
    }

    if st.session_state.get("video_menu"):
        st.subheader(f"📺 {st.session_state.video_menu} 영상")

        for title, v in video_map.get(st.session_state.video_menu, []):
            st.markdown(f"<div style='font-size:15px; font-weight:700; margin-bottom:5px;'>🎬 {title}</div>", unsafe_allow_html=True)
            st.video(v)
            st.divider()

    st.markdown("### 📄 서류 자료")

    if st.button("안전교육 서류(신규자)", key="d1"):
        st.session_state.doc_menu = "안전교육 서류(신규자)"

    if st.button("친절 및 안전교육 서류", key="d2"):
        st.session_state.doc_menu = "친절 및 안전교육 서류"

    st.divider()

    doc_map = {
        "안전교육 서류(신규자)": [
            ("신규자 교육일지(신규)", "docs/신규자 교육일지(신규).xlsx"),
            ("신규자 교육일지(특별)", "docs/신규자 교육일지(특별).xlsx"),
            ("안전보건교육 확인서", "docs/안전보건교육 확인서.xlsx"),
        ],
        "친절 및 안전교육 서류": [
            ("친절 및 안전교육", "docs/친절교육 및 안전교육.xlsx"),
        ],
    }

    if st.session_state.get("doc_menu"):
        st.subheader(f"📑 {st.session_state.doc_menu}")

        for title, path in doc_map.get(st.session_state.doc_menu, []):
            st.markdown(f"<div style='font-size:15px; font-weight:700; margin-bottom:5px;'>📄 {title}</div>", unsafe_allow_html=True)

            if path.endswith(".pdf"): mime_type = "application/pdf"
            elif path.endswith(".xlsx"): mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif path.endswith(".xls"): mime_type = "application/vnd.ms-excel"
            else: mime_type = "application/octet-stream"

            with open(path, "rb") as file:
                st.download_button(
                    label="다운로드",
                    data=file,
                    file_name=path.split("/")[-1],
                    mime=mime_type,
                    key=f"doc_{title}"
                )
            st.divider()


# =========================
# 선택 공종 & 세부공종 로직
# =========================
defect_type = st.session_state.defect_type

if defect_type is None and st.session_state.video_menu is None and st.session_state.doc_menu is None:
    st.markdown(
        "<h3 style='text-align:center; color:orange; margin-top:40px;'>⚠️ 공종을 먼저 선택하세요</h3>",
        unsafe_allow_html=True
    )
    st.stop()

sub_work_map = {
    "타일공사": ["타일교체", "마감공사"],
    "방수공사": ["액체방수", "도막방수", "복합방수"],
    "미장공사": ["미장공사", "견출공사"],
    "도장공사": ["도장공사"],
    "내장공사": ["석고공사", "단열공사", "걸레받이공사"],
    "도배공사": ["도배공사"],
    "마루공사": ["마루공사"],
    "가구공사": ["문짝공사", "시스템가구"],
    "창호공사": ["방충망교체"],
    "금속공사": ["금속공사"],
    "전기공사": ["차단기교체", "스위치,콘센트교체"],
    "설비공사": ["배관공사", "도기교체"],
}

sub_list = sub_work_map.get(defect_type, [])
sub_work = "선택하세요"

if defect_type is not None:
    if len(sub_list) == 1 and sub_list[0] == defect_type:
        sub_work = defect_type
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        sub_work = st.selectbox(
            "세부 공종 선택",
            ["선택하세요"] + sub_list,
            key="sub_work_select"
        )

# =========================
# 데이터베이스
# =========================
material_db = {
    "타일교체": ["타일(도기질/자기질)", "타일접착제(에폭시 본드,우레탄 실리콘, 압착 본드, 접착 몰탈)", "타일절단기", "실리콘", "실리콘건", "망치", "고무망치", "드라이버", "그라인더", "고무헤라", "줄눈재", "보양비닐", "청소기"],
    "마감공사": ["줄눈재", "고무헤라", "실리콘", "실리콘건", "백업재", "마스킹테이프"],
    "액체방수": ["시멘트계 액체방수재", "몰탈", "프라이머", "보강메쉬", "방수테이프", "붓", "교반기", "흙손", "양동이"],
    "도막방수": ["우레탄 방수재(하도/중도/상도)", "균열보수용 퍼티", "우레탄 실리콘", "실리콘건", "롤러", "붓", "헤라", "교반기", "양동이", "마스킹테이프", "보양비닐", "청소도구"],
    "복합방수": ["방수시트(PVC시트/아스팔트시트 등)", "도막방수제(우레탄/시멘트계)", "프라이머", "코너보강재", "시트접착제", "실리콘건", "실리콘", "백업재", "균열보수용 퍼티", "압착롤러", "헤라", "교반기", "양동이"],
    "미장공사": ["미장몰탈", "레미탈", "메쉬테이프", "프라이머", "퍼티", "균열보수재", "쇠흙손", "미장칼", "교반기", "양동이", "스펀지"],
    "견출공사": ["견출몰탈", "메쉬테이프", "균열보수재", "퍼티", "사포", "쇠흙손", "미장칼", "고무헤라", "스펀지", "교반기", "양동이"],
    "도장공사": ["페인트(수성/유성/내부용/외부용)", "중도/상도 페인트", "프라이머", "퍼티", "사포", "균열보수재", "실리콘", "롤러", "붓", "페인트 트레이", "마스킹테이프", "보양비닐"],
    "석고공사": ["석고보드", "피스", "퍼티", "수평대", "실리콘", "실리콘건", "줄자"],
    "단열공사": ["열화상카메라", "석고보드", "쥐꼬리톱", "꺽쇠", "실리콘", "실리콘건", "우레탄폼", "폼건", "피스", "퍼티", "비닐보양"],
    "걸레받이공사": ["걸레받이", "절단기", "헤라", "실리콘", "실리콘건", "글루건", "비닐보양"],
    "도배공사": ["도배지(벽지/천장지)", "도배풀", "퍼티", "초배지", "균열보수재", "실리콘", "도배솔", "롤러", "칼받이"],
    "마루공사": ["마루(강마루, 온돌마루)", "마루접착제", "정", "망치", "스크래퍼", "순간접착제", "고무망치", "비닐보양"],
    "문짝공사": ["경첩(무댐퍼/유압댐퍼)", "전동드릴"],
    "시스템가구": ["전동드릴", "사다리", "피스보관통"],
    "방충망교체": ["방충망 롤러", "가위"],
    "금속공사": ["철재/스텐인리스(각파이프, 앵글)", "앵커볼트", "볼트/너트/와셔", "피스", "용접봉", "방청도료", "페인트", "실리콘", "실리콘건", "그라인더", "절단기", "수평자"],
    "차단기교체": ["차단기", "검지기", "드라이버", "전동드릴", "절연테이프", "가위"],
    "스위치,콘센트교체": ["스위치/콘센트", "검지기", "드라이버", "펜치", "가위", "절연테이프"],
    "배관공사": ["배관(PVC/PB/PE/동관/주름관)", "엘보", "소켓/커플링", "벨브류", "트랩", "본드", "테이프", "실리콘", "패킹", "보온재", "파이프커터", "렌치/몽키스페너", "전동드릴", "수평자", "열융착기"],
    "도기교체": ["양변기", "세면대", "플렉시블 호수", "앵글벨브", "연결소켓", "트렙", "실리콘", "테프론테이프", "패킹", "앙카볼트", "피스", "수평자", "몽키스페너", "전동드릴"],
}

video_db = {
    "타일교체": [("타일 교체 작업", "https://www.youtube.com/watch?v=WKbH5jPpGy4")],
    "마감공사": [("타일 줄눈 및 실리콘 보수 작업", "https://www.youtube.com/watch?v=TQTivmeSWEc")],
    "석고공사": [("석고보드 교체 작업", "https://www.youtube.com/watch?v=wWAZ0Q44geg")],
    "단열공사": [("결로 보수 작업", "https://www.youtube.com/watch?v=0e4xNMnbkJE")],
    "걸레받이공사": [("걸레받이 보수 작업", "https://www.youtube.com/watch?v=wg47rdHW9bA")],
    "도배공사": [("도배 보수 작업", "https://www.youtube.com/watch?v=PcDamU1lSmg")],
    "마루공사": [("마루 교체 작업", "https://www.youtube.com/watch?v=m6f79GAquKk"), ("마루 부분 보수 작업", "https://www.youtube.com/watch?v=BrW02RHczL8")],
    "문짝공사": [("가구 문짝 교체 작업", "https://www.youtube.com/watch?v=lTlDmcsCU4g")],
    "시스템가구": [("시스템가구 설치 및 해체 작업", "https://www.youtube.com/watch?v=x7VeChdlMM4")],
    "방충망교체": [("방충망 교체 작업", "https://www.youtube.com/watch?v=oIO83G6Mgws")],
    "차단기교체": [("분전반 차단기 교체 작업", "https://www.youtube.com/watch?v=npnUZc6fRyI")],
    "스위치,콘센트교체": [("스위치, 콘센트 교체 작업", "https://www.youtube.com/watch?v=8wr7L-U0v1g")],
}

process_db = {
    "액체방수": ["바탕면 정리(이물질, 레이턴스 제거, 균열부 보수)※주의사항 : 바탕 불량 시, 들뜸 발생", "바탕면 건조 확인(자연건조 및 송풍기 사용)※주의사항 : 건조 불량 시, 접착력 저하 발생", "프라이머 도포(롤러 또는 붓으로 균일하게 도포)", "코너 보강 작업(라운딩 처리)", "1차 방수(규정 두께로 균일하게 도포)", "2차 방수", "양생", "담수 시험"],
    "도막방수": ["바탕면 정리(이물질, 레이턴스 제거)※주의사항 : 바탕불량 = 들뜸 발생", "크랙 및 파손부 보수(퍼티)", "바탕면 건조 확인(함수율 체크)※주의사항 : 습기 → 기포 발생 원인", "프라이머(하도) 도포", "코너 보강 작업", "중도 도포(규정 두께 확보)", "상도 도포", "양생"],
    "복합방수": ["바탕면 정리(이물질, 레이턴스 제거, 균열부 보수)※바탕불량 : 시트들뜸 발생", "바탕면 건조 확인(함수율 체크)※주의사항 : 습기 → 접착불량 및 기포 발생", "프라이머 도포", "코너 보강 작업(코너 및 배수구 주변 작업)", "시트 부착(겹침부 50~100mm 확보)", "시트 이음부 보강", "중도 도포", "상도 도포", "양생", "보호층시공"],
    "미장공사": ["바탕면 정리(이물질, 레이턴스 제거)※주의사항 : 바탕불량 = 들뜸 발생", "균열 및 결손부 보수(크랙 : 메쉬테이프+보수몰탈)", "바탕면 습윤 처리", "프라이머 도포", "기준 먹매김", "초벌 미장(거칠게 정리)", "정벌 미장(표면 평활도 주의)", "양생"],
    "견출공사": ["바탕면 정리(이물질, 레이턴스 제거)※주의사항 : 바탕불량 = 탈락 발생", "균열 및 파손부 보수", "프라이머 도포", "초벌 작업(면잡기)", "정벌 작업(마감)", "표면 정리", "양생"],
    "도장공사": ["바탕면정리(이물질 제거)※주의사항 : 바탕불량 = 도장 박리/들뜸 발생", "균열 및 결손부 보수", "샌딩(사포 작업)", "프라이머 도포", "중도 도장", "상도 도장(균일한 롤링 작업)", "양생"],
    "금속공사": ["바탕면 정리(콘크리트면 이물질 제거)※주의사항 : 앵커 고정력 확보 중요", "앵커 및 베이스 고정 ※주의사항 : 고정불량 = 구조 불안정", "금속 부재 가공 및 설치", "용접 작업", "용접부 정리(그라인딩)", "방청 처리(미도포 시 부식 발생)", "도장 마감", "마감 및 정리"],
    "배관공사": ["바탕면 및 시공부 준비※주의사항 : 구조체 손상 주의", "배관 자재 가공(배관 절단)※주의사항 : 절단면 불량 = 누수 원인", "배관 연결작업(PVC = 본드접합, PB/PE = 열융착, 동관 = 용접 또는 압착)※주의사항 : 접합불량 = 누수 1순위", "배관 설치 및 고정", "기기 및 도기 연결", "보온 및 마감", "압력 및 통수 시험(급수 = 압력테스트, 배수 = 통수시험)", "최종 점검 및 정리"],
    "도기교체": ["설치 위치 확인", "배관 상태 점검※주의사항 : 배관 문제 있으면 먼저 보수", "설치 전 준비(주변 청소, 연결 부품 준비)", "도기 설치(위치 잡기, 수평 확인)", "고정 작업(앙카 및 피스 고정)", "급수 및 배수 연결", "실리콘 마감", "통수 및 누수 시험", "최종 점검 및 정리"],
}

warranty_db = {
    "타일교체": "키불출일 부터 2년(입주자 과실 제외)",
    "마감공사": "키불출일 부터 2년(입주자 과실 제외)",
    "액체방수": "키불출일 부터 5년(입주자 과실 제외)",
    "도막방수": "키불출일 부터 5년(입주자 과실 제외)",
    "복합방수": "키불출일 부터 5년(입주자 과실 제외)",
    "미장공사": "키불출일 부터 2년(입주자 과실 제외)",
    "견출공사": "키불출일 부터 2년(입주자 과실 제외)",
    "도장공사": "키불출일 부터 2년(입주자 과실 제외)",
    "석고공사": "키불출일 부터 2년(입주자 과실 제외)",
    "단열공사": "키불출일 부터 3년(입주자 과실 제외)",
    "걸레받이공사": "키불출일 부터 2년(입주자 과실 제외)",
    "도배공사": "키불출일 부터 2년(입주자 과실 제외)",
    "마루공사": "키불출일 부터 2년(입주자 과실 제외)",
    "문짝공사": "키불출일 부터 2년(입주자 과실 제외)",
    "시스템가구": "키불출일 부터 2년(입주자 과실 제외)",
    "방충망교체": "키불출일 부터 3년(입주자 과실 제외)",
    "금속공사": "키불출일 부터 3년(입주자 과실 제외)",
    "차단기교체": "키불출일 부터 3년(입주자 과실 제외)",
    "스위치,콘센트교체": "키불출일 부터 3년(입주자 과실 제외)",
    "배관공사": "키불출일 부터 3년(입주자 과실 제외)",
    "도기교체": "키불출일 부터 3년(입주자 과실 제외)",
}

# =========================
# 검색 버튼 (가운데 정렬)
# =========================
search_btn = False

if defect_type is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 화면을 좌/중/우 3등분해서 가운데 공간에만 버튼을 배치합니다.
    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_center:
        search_btn = st.button("🔍 검색 실행", use_container_width=True)

# =========================
# 검색 처리
# =========================
if search_btn:
    if len(sub_list) > 1 and sub_work == "선택하세요":
        st.markdown("""
        <div class="warning-banner">
            ⚠️ 세부공종을 먼저 선택하세요
        </div>
        """, unsafe_allow_html=True)
        st.session_state.search_clicked = False
    else:
        st.session_state.search_clicked = True

# =========================
# 결과 출력
# =========================
if st.session_state.search_clicked and sub_work != "선택하세요":

    # 담보책임기간
    st.subheader("🛡️ 담보책임기간(공동주택관리법 제36조)")

    period = warranty_db.get(sub_work)

    if period:
        st.markdown(f"""
        <div style="
            padding:12px;
            margin:8px 0;
            border-radius:10px;
            background-color:#e7f5ff;
            border-left:5px solid #339af0;
            font-weight:600;
            font-size:16px;
            text-align:center;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
            word-break: keep-all;
        ">
            {sub_work} : {period}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("담보책임기간 정보 없음")

    st.divider()

    # 필요 자재
    st.subheader("🔧 필요 자재")

    if sub_work in material_db:
        materials = material_db.get(sub_work, [])

        html = '<div class="material-wrapper">'

        for m in materials:
            html += (
                '<div class="material-card">'
                f'{m}'
                '</div>'
            )

        html += '</div>'

        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("자재 정보 없음")

    st.divider()

    # 영상 자료
    st.subheader("🎬 영상 자료")

    videos = video_db.get(sub_work)
    has_guide_video = bool(videos)

    if videos:
        for title, url in videos:
            st.markdown(f"#### {title}")
            st.video(url)
            st.divider()

    # 작업 가이드
    if not has_guide_video:
        st.subheader("📋 작업 가이드")

        process = process_db.get(sub_work)

        if process:
            for i, step in enumerate(process, 1):
                st.markdown(f"""
                <div style="
                    padding:12px;
                    margin:8px 0;
                    border-radius:10px;
                    background-color:#fff7ed;
                    border-left:5px solid #FFA94D;
                    line-height:1.5;
                    font-size: 15px;
                ">
                    <b style="color: #d97706;">🔹 STEP {i}</b><br><br>
                    {step}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("작업순서 정보 없음")
