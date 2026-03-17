# database.py
# Reference: docs/architecture.md (File Responsibility Map)
# Reference: docs/api_reference.md (SQLite section)

import sqlite3, json
from datetime import datetime

DB_FILE = "epiclimate.db"


def init_db():
    """Creates DB and table if they don't exist. Safe to call multiple times."""
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id                       INTEGER PRIMARY KEY AUTOINCREMENT,
            run_timestamp            TEXT,
            region_name              TEXT,
            country                  TEXT,
            disease                  TEXT,
            lat                      REAL,
            lon                      REAL,
            current_temp_c           REAL,
            historical_avg_temp_c    REAL,
            temp_anomaly_c           REAL,
            current_precip_mm        REAL,
            historical_avg_precip_mm REAL,
            precip_anomaly_mm        REAL,
            current_humidity_pct     REAL,
            climate_anomaly_level    TEXT,
            anomaly_reasoning        TEXT,
            historical_risk_level    TEXT,
            recent_trend             TEXT,
            correlation_score        INTEGER,
            scientific_reasoning     TEXT,
            risk_score               INTEGER,
            confidence               TEXT,
            predicted_window         TEXT,
            key_factors              TEXT,
            high_risk_zones          TEXT,
            population_at_risk       TEXT,
            recommended_actions      TEXT,
            urgency_level            TEXT,
            lead_time_weeks          INTEGER,
            alert_text               TEXT,
            active_outbreak        INTEGER,
            recent_alert_count     INTEGER,
            is_real_data           INTEGER,
            data_sources           TEXT,
            real_world_advisories  TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[DB] epiclimate.db ready.")


def save_prediction(data: dict):
    """Saves one full pipeline result. Missing fields stored as NULL."""
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute("""
        INSERT INTO predictions (
            run_timestamp, region_name, country, disease, lat, lon,
            current_temp_c, historical_avg_temp_c, temp_anomaly_c,
            current_precip_mm, historical_avg_precip_mm, precip_anomaly_mm,
            current_humidity_pct, climate_anomaly_level, anomaly_reasoning,
            historical_risk_level, recent_trend, correlation_score,
            scientific_reasoning, risk_score, confidence, predicted_window,
            key_factors, high_risk_zones, population_at_risk,
            recommended_actions, urgency_level, lead_time_weeks, alert_text,
            active_outbreak, recent_alert_count, is_real_data,
            data_sources, real_world_advisories
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        datetime.now().isoformat(),
        data.get("region_name"),       data.get("country"),
        data.get("disease"),           data.get("lat"),
        data.get("lon"),               data.get("current_temp_c"),
        data.get("historical_avg_temp_c"), data.get("temp_anomaly_c"),
        data.get("current_precip_mm"), data.get("historical_avg_precip_mm"),
        data.get("precip_anomaly_mm"), data.get("current_humidity_pct"),
        data.get("anomaly_level"),     data.get("reasoning"),
        data.get("historical_risk_level"), data.get("recent_trend"),
        data.get("correlation_score"), data.get("scientific_reasoning"),
        data.get("risk_score"),        data.get("confidence"),
        data.get("predicted_window"),  json.dumps(data.get("key_factors", [])),
        json.dumps(data.get("high_risk_zones", [])),
        data.get("population_at_risk_estimate"),
        json.dumps(data.get("recommended_actions", [])),
        data.get("urgency_level"),     data.get("lead_time_weeks"),
        data.get("alert_text"),
        int(data.get("active_outbreak", False)),
        data.get("recent_alert_count", 0),
        int(data.get("is_real_data", False)),
        json.dumps(data.get("data_sources", [])),
        data.get("real_world_advisories", "none found"),
    ))
    conn.commit()
    conn.close()
    print(f"  [DB] Saved: {data.get('region_name')} / {data.get('disease')}")


def get_all_predictions() -> list:
    """Returns all saved predictions as a list of dicts, newest first."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions ORDER BY run_timestamp DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
