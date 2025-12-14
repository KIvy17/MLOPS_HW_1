import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth

API_URL = "http://ml_api:8000"

st.set_page_config(page_title="ML Dashboard", layout="wide")
st.title("🧠 Machine Learning Model Management Dashboard")

# -------------------- AUTH --------------------
st.sidebar.header("🔐 Авторизация")
username = st.sidebar.text_input("Username", "admin")
password = st.sidebar.text_input("Password", "admin", type="password")
AUTH = HTTPBasicAuth(username, password)

# -------------------- MENU --------------------
st.sidebar.header("📌 Меню")
page = st.sidebar.radio(
    "Выберите раздел:",
    [
        "Проверка сервиса",
        "Список моделей",
        "Обучить модель",
        "Предсказать",
        "Удалить модель",
    ],
)

# -------------------- HEALTH --------------------
if page == "Проверка сервиса":
    st.subheader("Проверка состояния API")
    resp = requests.get(f"{API_URL}/health")
    st.write(resp.json())

# -------------------- LIST MODELS --------------------
elif page == "Список моделей":
    st.subheader("📄 Сохранённые модели")
    resp = requests.get(f"{API_URL}/api/models", auth=AUTH)
    if resp.ok:
        models = resp.json().get("models", [])
        df = pd.DataFrame(models, columns=["Model ID"])
        st.table(df)
    else:
        st.error(resp.text)

# -------------------- TRAIN MODEL --------------------
elif page == "Обучить модель":
    st.subheader("📚 Обучение модели")

    model_type = st.selectbox(
        "Тип модели:", ["LogisticRegression", "RandomForestClassifier"]
    )

    uploaded_file = st.file_uploader("Загрузите CSV с данными", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📊 Данные:")
        st.dataframe(df)

        target_col = st.selectbox("Выберите колонку target:", df.columns)

        # Графики
        st.write("📉 Распределение target:")
        fig, ax = plt.subplots()
        df[target_col].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

        X = df.drop(columns=[target_col])
        y = df[target_col]

        # ----- HYPERPARAMETERS -----
        st.subheader("⚙ Гиперпараметры модели")

        if model_type == "LogisticRegression":
            max_iter = st.number_input("max_iter", 50, 2000, 100)
            C = st.slider("C (регуляризация)", 0.001, 5.0, 1.0)
            hyperparams = {"max_iter": int(max_iter), "C": float(C)}

        elif model_type == "RandomForestClassifier":
            n_estimators = st.slider("n_estimators", 10, 500, 100)
            max_depth = st.slider("max_depth", 1, 50, 10)
            hyperparams = {
                "n_estimators": int(n_estimators),
                "max_depth": int(max_depth),
            }

        if st.button("🚀 Обучить модель"):
            payload = {
                "train": X.values.tolist(),
                "target": y.values.tolist(),
                "model_type": model_type,
                "hyperparams": hyperparams,
            }
            resp = requests.post(f"{API_URL}/api/train", json=payload, auth=AUTH)
            st.write(resp.json())

# -------------------- PREDICT --------------------
elif page == "Предсказать":
    st.subheader("🔮 Предсказание")

    model_id = st.text_input("Введите ID модели:")

    uploaded_file = st.file_uploader("Загрузите CSV для предсказания", type=["csv"])

    if uploaded_file and model_id:
        df = pd.read_csv(uploaded_file)
        st.write("📊 Данные для предсказания:")
        st.dataframe(df)

        if st.button("Сделать предсказание"):
            payload = {"data": df.values.tolist()}
            resp = requests.post(
                f"{API_URL}/api/predict/{model_id}", json=payload, auth=AUTH
            )
            result = resp.json()
            preds = result.get("predictions", [])
            df["prediction"] = preds
            st.write("🔮 Результаты предсказаний:")
            st.dataframe(df)

# -------------------- DELETE MODEL --------------------
elif page == "Удалить модель":
    st.subheader("🗑 Удаление модели")

    model_id = st.text_input("ID модели для удаления")

    if st.button("Удалить"):
        resp = requests.delete(f"{API_URL}/api/delete/{model_id}", auth=AUTH)
        st.write(resp.json())
