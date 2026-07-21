import streamlit as st
from openai import OpenAI

# OpenAI API
ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 세션 상태
if "book_list" not in st.session_state:
    st.session_state.book_list = []

if "reading_goal" not in st.session_state:
    st.session_state.reading_goal = "하루 30분 독서하기"


def add_book():
    book = st.session_state.book_input
    if book:
        st.session_state.book_list.append([book, False])
        st.toast("읽을 책이 추가되었습니다!")
        st.session_state.book_input = ""


# 1. 독서 목표
def page_goal():
    st.header("📚 1. 오늘의 독서 목표")

    goal = st.text_input("오늘의 독서 목표를 입력하세요")

    if st.button("목표 저장"):
        st.session_state.reading_goal = goal
        st.success("목표가 저장되었습니다!")


# 2. 읽을 책
def page_books():
    st.header("📖 2. 읽을 책 목록")

    st.write(f"오늘의 목표 : **{st.session_state.reading_goal}**")

    st.text_input("읽을 책을 입력하세요", key="book_input")
    st.button("추가하기", on_click=add_book)

    st.markdown("---")

    for i in range(len(st.session_state.book_list)):
        col1, col2, col3 = st.columns([4,1,1])

        with col1:
            st.write(f"{i+1}. {st.session_state.book_list[i][0]}")

        with col2:
            if st.button("완독", key=f"finish{i}"):
                st.session_state.book_list[i][1] = True
                st.rerun()

        with col3:
            if st.session_state.book_list[i][1]:
                st.write("📕 완료!")


# 3. 독서 달성률
def page_report():
    st.header("📊 3. 독서 달성률")

    if len(st.session_state.book_list) == 0:
        st.write("등록된 책이 없습니다.")
    else:
        total = len(st.session_state.book_list)
        count = sum(item[1] for item in st.session_state.book_list)

        progress = count / total

        st.metric("완독률", f"{progress*100:.1f}%")
        st.progress(progress)

        if st.button("목록 초기화"):
            st.session_state.book_list = []
            st.rerun()


# 4. AI 독서 코칭
def page_ai_coach():
    st.header("🤖 AI 독서 코치")

    prompt = st.text_input("독서 관련 질문을 입력하세요")

    if st.button("질문하기"):
        if prompt.strip() == "":
            st.warning("질문을 입력해주세요.")
        else:
            try:
                response = ai_client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )
                st.write(response.output_text)

            except Exception as e:
                st.error(e)


# 페이지
pg = st.navigation([
    st.Page(page_goal, title="독서 목표", icon="🎯"),
    st.Page(page_books, title="읽을 책", icon="📚"),
    st.Page(page_report, title="독서 달성률", icon="📊"),
    st.Page(page_ai_coach, title="AI 독서 코치", icon="🤖"),
], position="top")

st.title("📚 독서 습관 플래너")

pg.run()
