import streamlit as st

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

st.set_page_config(layout="centered")

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
# 전체 스타일
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f8f9fa;
}

.block-container {
    max-width: 1100px;
    margin: 0 auto;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* 메인 버튼 */
div.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffa94d, #ff922b);
    color: white;
    font-size: 20px;
    font-weight: 900;
    border: none;
    margin: 8px 6px 12px 6px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

/* 경고 배너 */
.warning-banner {
    width: 100%;
    text-align: center;
    color: #856404;
    background-color: #fff3cd;
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

/* 자재 카드 */
.material-wrapper {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 10px;
}

.material-card {
    background: linear-gradient(135deg, #ffffff, #f1f3f5);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid #e9ecef;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    transition: all 0.25s ease;
    cursor: pointer;
}

.material-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    border-color: #FFA94D;
    background: linear-gradient(135deg, #fff4e6, #ffe8cc);
}

.material-icon {
    font-size: 26px;
    margin-bottom: 8px;
}

.material-title {
    word-break: keep-all;
    line-height: 1.4;
}

/* 사이드바 버튼 */
section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    padding: 25px;
    margin-bottom: 14px;
    border-radius: 20px;
    border: 1px solid #e9ecef;
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    font-size: 14px;
    font-weight: 800;
    color: #212529 !important;
    transition: all 0.25s ease;
}

/* selectbox 라벨 조금 강조 */
label[data-baseweb="select"] + div,
div[data-baseweb="select"] {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 메인 중앙 레이아웃
# =========================
main_left, main_center, main_right = st.columns([1, 8, 1])

# =========================
# 상단 헤더
# =========================
with main_center:
    st.image("lynn.png", width=100)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="max-width:700px; margin:0 auto; text-align:center;">
        <h1 style="
            margin:0;
            position: relative;
            left: -30px;
        ">
            전유부 공종별 작업 메뉴얼
        </h1>
        <p style="
            font-size:30px;
            font-weight:700;
            margin-top:10px;
            margin-bottom:0;
            position: relative;
            left: -45px;
        ">
            ※공종 선택※
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 공종 버튼
# =========================
with main_center:
    cols = st.columns(4)

    types = [
        "타일공사", "방수공사", "미장공사", "도장공사",
        "내장공사", "도배공사", "마루공사", "가구공사",
        "창호공사", "금속공사", "전기공사", "설비공사"
    ]

    for i, t in enumerate(types):
        with cols[i % 4]:
            if st.button(t, key=f"type_{i}"):
                st.session_state.defect_type = t
                st.session_state.search_clicked = False
                st.session_state.video_menu = None
                st.session_state.doc_menu = None

with main_center:
    if st.session_state.defect_type:
        st.markdown(f"""
        <div style="
            max-width:700px;
            margin:0 auto;
            text-align:center;
            position: relative;
            left: -45px;
        ">
            <p style='font-size:18px; font-weight:600; margin-top:10px;'>
                선택 공종 : <span style='color:#ff922b'>{st.session_state.defect_type}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================
# 사이드바
# =========================
with st.sidebar:
    st.markdown("### ⚙️ 설정")

    if st.button("🔄 전체 초기화"):
        st.session_state.defect_type = None
        st.session_state.search_clicked = False
        st.session_state.video_menu = None
        st.session_state.doc_menu = None
        st.rerun()

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
            st.markdown(
                f"""
                <div style="
                    font-size:16px;
                    font-weight:700;
                    margin-bottom:5px;
                ">
                    🎬 {title}
                </div>
                """,
                unsafe_allow_html=True
            )
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
            st.markdown(
                f"""
                <div style="
                    font-size:16px;
                    font-weight:700;
                    margin-bottom:5px;
                ">
                    📄 {title}
                </div>
                """,
                unsafe_allow_html=True
            )

            if path.endswith(".pdf"):
                mime_type = "application/pdf"
            elif path.endswith(".xlsx"):
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif path.endswith(".xls"):
                mime_type = "application/vnd.ms-excel"
            else:
                mime_type = "application/octet-stream"

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
# 선택 공종
# =========================
defect_type = st.session_state.defect_type

if defect_type is None and st.session_state.video_menu is None and st.session_state.doc_menu is None:
    with main_center:
        st.markdown(
            "<h3 style='text-align:center; color:orange; margin-top:30px;'>⚠️ 공종 먼저 선택하세요</h3>",
            unsafe_allow_html=True
        )
    st.stop()

# =========================
# 세부공종 데이터
# =========================
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

# =========================
# 세부공종 선택
# =========================
# =========================
# 세부공종 선택
# =========================
sub_work = "선택하세요"

if defect_type is not None:
    if len(sub_list) == 1 and sub_list[0] == defect_type:
        sub_work = defect_type
    else:
        with main_center:
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
# 검색 버튼
# =========================
search_btn = False

if defect_type is not None:
    with main_center:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_left, btn_center, btn_right = st.columns([2.5, 2, 2.5])
        with btn_center:
            search_btn = st.button("🔍 검색 실행")

# =========================
# 검색 처리
# =========================
if search_btn:
    if len(sub_list) > 1 and sub_work == "선택하세요":
        with main_center:
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
with main_center:
    if st.session_state.search_clicked and sub_work != "선택하세요":

        # 담보책임기간
        st.subheader("🛡️ 담보책임기간(공동주택관리법 제36조 제1항 제2호)")

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
                font-size:18px;
                text-align:center;
                box-shadow:0 2px 6px rgba(0,0,0,0.1);
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
                    f'<div class="material-title">{m}</div>'
                    '</div>'
                )

            html += '</div>'

            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("자재 정보 없음")

        st.divider()

        # 영상 자료
        st.subheader("영상 자료")

        videos = video_db.get(sub_work)
        has_guide_video = bool(videos)

        if videos:
            for title, url in videos:
                st.markdown(f"### 🎬 {title}")
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
                        margin:6px 0;
                        border-radius:10px;
                        background-color:#fff7ed;
                        border-left:5px solid #FFA94D;
                        line-height:1.6;
                    ">
                        <b>🔹 STEP {i}</b><br><br>
                        {step}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("작업순서 정보 없음")
