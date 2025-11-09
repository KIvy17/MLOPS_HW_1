import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="ML Service Dashboard", layout="centered")
st.title("🧠 ML Service Dashboard")

token = st.text_input("🔑 Введите JWT токен", type="password")

if token:
    headers = {"Authorization": f"Bearer {token}"}
    st.sidebar.header("Меню")
    action = st.sidebar.selectbox("Выберите действие", ["Проверить сервис", "Список моделей", "Обучить", "Предсказать", "Удалить"])

    if action == "Проверить сервис":
        resp = requests.get(f"{API_URL}/health")
        st.write(resp.json())

    elif action == "Список моделей":
        resp = requests.get(f"{API_URL}/models", headers=headers)
        st.write(resp.json() if resp.ok else resp.text)

    elif action == "Обучить":
        model_type = st.selectbox("Тип модели", ["LogisticRegression", "RandomForestClassifier"])
        X_text = st.text_area("X (пример: [[1,2],[2,3],[3,4]])", "[[1,2],[2,3],[3,4]]")
        y_text = st.text_input("y (пример: [0,1,0])", "[0,1,0]")
        if st.button("Обучить модель"):
            try:
                X = eval(X_text)
                y = eval(y_text)
                data = {"model_type": model_type, "X": X, "y": y}
                resp = requests.post(f"{API_URL}/train", json=data, headers=headers)
                st.write(resp.json())
            except Exception as e:
                st.error(str(e))

    elif action == "Предсказать":
        model_id = st.text_input("ID модели")
        X_text = st.text_area("X (пример: [[1,2],[2,3]])", "[[1,2],[2,3]]")
        if st.button("Предсказать"):
            try:
                X = eval(X_text)
                data = {"X": X}
                resp = requests.post(f"{API_URL}/predict/{model_id}", json=data, headers=headers)
                st.write(resp.json())
            except Exception as e:
                st.error(str(e))

    elif action == "Удалить":
        model_id = st.text_input("ID модели для удаления")
        if st.button("Удалить модель"):
            resp = requests.delete(f"{API_URL}/delete/{model_id}", headers=headers)
            st.write(resp.json())
else:
    st.info("Введите JWT токен для доступа (получить через /token в API).")
