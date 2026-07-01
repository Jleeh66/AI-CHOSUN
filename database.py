# database.py
# 데이터베이스 생성, 저장, 조회 기능을 담당하는 파일

import sqlite3
import pandas as pd
import os
from datetime import datetime   # 현재 날짜/시간을 가져오는 라이브러리


# ──────────────────────────────────────────
# 설정값
# ──────────────────────────────────────────
DB_FOLDER = "data"
DB_PATH   = os.path.join(DB_FOLDER, "ship_fuel.db")


def create_database():
    """
    데이터베이스와 테이블을 생성하는 함수.
    이미 존재하면 다시 만들지 않음 (IF NOT EXISTS).
    """
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    connection = sqlite3.connect(DB_PATH)
    cursor     = connection.cursor()

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS fuel_records (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            ship_name        TEXT    NOT NULL,
            distance         REAL    NOT NULL,
            speed            REAL    NOT NULL,
            operation_hours  REAL    NOT NULL,
            fuel_per_hour    REAL    NOT NULL,
            fuel_price       REAL    NOT NULL,
            total_fuel       REAL    NOT NULL,
            total_cost       REAL    NOT NULL,
            created_at       TEXT    NOT NULL
        )
    """

    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()


def save_record(
    ship_name      : str,
    distance       : float,
    speed          : float,
    operation_hours: float,
    fuel_per_hour  : float,
    fuel_price     : float,
    total_fuel     : float,
    total_cost     : float
) -> bool:
    """
    계산 결과를 데이터베이스에 저장하는 함수.

    Args:
        ship_name       (str)  : 선박명
        distance        (float): 운항 거리 (km)
        speed           (float): 평균 속도 (km/h)
        operation_hours (float): 운항 시간 (hour)
        fuel_per_hour   (float): 시간당 연료 소비량 (L/h)
        fuel_price      (float): 연료 단가 (원/L)
        total_fuel      (float): 총 연료 소비량 (L)
        total_cost      (float): 총 운항 비용 (원)

    Returns:
        bool: 저장 성공 시 True, 실패 시 False
    """
    try:
        # 현재 날짜와 시간을 문자열로 변환
        # 예 : "2025-01-15 14:30:00"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection = sqlite3.connect(DB_PATH)
        cursor     = connection.cursor()

        # INSERT SQL : 테이블에 새 행을 추가
        # ? 는 placeholder : 아래 튜플의 값이 순서대로 들어감
        insert_sql = """
            INSERT INTO fuel_records (
                ship_name,
                distance,
                speed,
                operation_hours,
                fuel_per_hour,
                fuel_price,
                total_fuel,
                total_cost,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # 튜플 순서가 위의 컬럼 순서와 반드시 일치해야 함
        values = (
            ship_name,
            distance,
            speed,
            operation_hours,
            fuel_per_hour,
            fuel_price,
            total_fuel,
            total_cost,
            created_at
        )

        cursor.execute(insert_sql, values)
        connection.commit()
        connection.close()

        return True   # 저장 성공

    except sqlite3.Error as e:
        # 데이터베이스 관련 오류 발생 시
        print(f"DB 저장 오류 : {e}")
        return False  # 저장 실패

def get_all_records() -> pd.DataFrame:
    """
    저장된 모든 기록을 불러오는 함수.
    최신 기록이 위에 오도록 내림차순 정렬합니다.

    Returns:
        pd.DataFrame: 전체 기록을 담은 데이터프레임.
                      데이터가 없으면 빈 데이터프레임 반환.
    """
    try:
        connection = sqlite3.connect(DB_PATH)

        select_sql = """
            SELECT
                id              AS 번호,
                ship_name       AS 선박명,
                distance        AS '운항거리(km)',
                speed           AS '평균속도(km/h)',
                operation_hours AS '운항시간(h)',
                fuel_per_hour   AS '시간당연료(L/h)',
                fuel_price      AS '연료단가(원/L)',
                total_fuel      AS '총연료(L)',
                total_cost      AS '총비용(원)',
                created_at      AS 저장일시
            FROM fuel_records
            ORDER BY id DESC
        """

        df = pd.read_sql_query(select_sql, connection)
        connection.close()

        return df

    except sqlite3.Error as e:
        print(f"DB 조회 오류 : {e}")
        return pd.DataFrame()


def delete_record(record_id: int) -> bool:
    """
    특정 번호의 기록을 삭제하는 함수.

    Args:
        record_id (int): 삭제할 기록의 id

    Returns:
        bool: 삭제 성공 시 True, 실패 시 False
    """
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor     = connection.cursor()

        delete_sql = "DELETE FROM fuel_records WHERE id = ?"
        cursor.execute(delete_sql, (record_id,))

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as e:
        print(f"DB 삭제 오류 : {e}")
        return False

# ──────────────────────────────────────────
# 테스트 코드
# ──────────────────────────────────────────
if __name__ == "__main__":

    # DB 초기화
    create_database()

    # 테스트 데이터 저장
    success = save_record(
        ship_name       = "독도호",
        distance        = 1500.0,
        speed           = 25.0,
        operation_hours = 60.0,
        fuel_per_hour   = 120.0,
        fuel_price      = 1800.0,
        total_fuel      = 7200.0,
        total_cost      = 12960000.0
    )

    if success:
        print("✅ 저장 성공!")
    else:
        print("❌ 저장 실패!")

    # 저장된 데이터 확인
    connection = sqlite3.connect(DB_PATH)
    cursor     = connection.cursor()
    cursor.execute("SELECT * FROM fuel_records")
    rows = cursor.fetchall()
    connection.close()

    print(f"\n📋 저장된 데이터 ({len(rows)}건)")
    for row in rows:
        print(row)