# charts.py
# 그래프를 그리는 함수를 담당하는 파일

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd


def set_korean_font():
    """
    matplotlib에서 한글이 깨지지 않도록 폰트를 설정하는 함수.
    Windows 환경에서는 'Malgun Gothic'(맑은 고딕)을 사용합니다.
    """
    plt.rcParams["font.family"]     = "Malgun Gothic"  # 맑은 고딕
    plt.rcParams["axes.unicode_minus"] = False          # 마이너스 기호 깨짐 방지


def draw_fuel_bar_chart(df: pd.DataFrame) -> plt.Figure:
    """
    선박별 총 연료 소비량을 비교하는 가로 막대 차트를 그리는 함수.

    Args:
        df (pd.DataFrame): get_all_records()가 반환한 데이터프레임

    Returns:
        plt.Figure: 그려진 그래프 객체 (st.pyplot()에 전달)
    """
    set_korean_font()

    fuel_by_ship = (
        df.groupby("선박명")["총연료(L)"]
        .mean()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.barh(
        fuel_by_ship.index,
        fuel_by_ship.values,
        color="#2196F3",
        alpha=0.8
    )

    for bar, value in zip(bars, fuel_by_ship.values):
        ax.text(
            value + max(fuel_by_ship.values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,.1f} L",
            va="center",
            fontsize=9
        )

    ax.set_title("선박별 평균 연료 소비량 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("총 연료 소비량 (L)", fontsize=10)
    ax.set_ylabel("선박명", fontsize=10)

    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )

    plt.tight_layout()

    return fig


def draw_cost_bar_chart(df: pd.DataFrame) -> plt.Figure:
    """
    선박별 총 운항 비용을 비교하는 가로 막대 차트를 그리는 함수.

    Args:
        df (pd.DataFrame): get_all_records()가 반환한 데이터프레임

    Returns:
        plt.Figure: 그려진 그래프 객체
    """
    set_korean_font()

    cost_by_ship = (
        df.groupby("선박명")["총비용(원)"]
        .mean()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.barh(
        cost_by_ship.index,
        cost_by_ship.values,
        color="#4CAF50",
        alpha=0.8
    )

    for bar, value in zip(bars, cost_by_ship.values):
        ax.text(
            value + max(cost_by_ship.values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{value / 10000:,.0f} 만원",
            va="center",
            fontsize=9
        )

    ax.set_title("선박별 평균 운항 비용 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("총 운항 비용 (원)", fontsize=10)
    ax.set_ylabel("선박명", fontsize=10)

    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}")
    )

    plt.tight_layout()

    return fig


def draw_cost_trend_chart(df: pd.DataFrame) -> plt.Figure:
    """
    저장 순서에 따른 운항 비용 추이를 꺾은선 차트로 그리는 함수.

    Args:
        df (pd.DataFrame): get_all_records()가 반환한 데이터프레임

    Returns:
        plt.Figure: 그려진 그래프 객체
    """
    set_korean_font()

    df_sorted = df.sort_values("번호").reset_index(drop=True)

    x_values = range(1, len(df_sorted) + 1)
    y_values = df_sorted["총비용(원)"].values

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        x_values,
        y_values,
        marker="o",
        color="#FF5722",
        linewidth=2,
        markersize=8
    )

    for x, y, name in zip(x_values, y_values, df_sorted["선박명"]):
        ax.annotate(
            f"{name}\n{y / 10000:,.0f}만원",
            xy=(x, y),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            fontsize=8
        )

    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    ax.set_title("운항 비용 추이", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("저장 순번", fontsize=10)
    ax.set_ylabel("총 운항 비용 (원)", fontsize=10)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:,.0f}")
    )

    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    return fig
