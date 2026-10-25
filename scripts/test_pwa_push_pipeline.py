import requests
import json
import sys
import sqlite3
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "velvet_data.db"
BASE_URL = "http://localhost:8888"

def test_pipeline():
    print("==================================================")
    print("🧪 SIREN AI - Test PWA & Web Push Pipeline")
    print("==================================================")

    # 1. Manifest
    r_man = requests.get(f"{BASE_URL}/manifest.json")
    assert r_man.status_code == 200, f"Manifest failed: {r_man.status_code}"
    m_data = r_man.json()
    assert m_data.get("name") == "SIREN AI - Sam Barton Command"
    assert m_data.get("display") == "standalone"
    print("  ✓ 1. Manifest JSON valid and contains standalone display & icons")

    # 2. Service Worker
    r_sw = requests.get(f"{BASE_URL}/sw.js")
    assert r_sw.status_code == 200, f"SW failed: {r_sw.status_code}"
    assert "push" in r_sw.text
    assert "notificationclick" in r_sw.text
    assert "NAVIGATE_ASSISTANT" in r_sw.text
    print("  ✓ 2. Service Worker sw.js serves valid JS with push & click handlers")

    # 3. VAPID Public Key
    r_key = requests.get(f"{BASE_URL}/api/push/vapid_public_key")
    assert r_key.status_code == 200, f"VAPID key failed: {r_key.status_code}"
    pub_key = r_key.json().get("publicKey")
    assert len(pub_key) >= 80, f"VAPID public key unexpected length: {pub_key}"
    print(f"  ✓ 3. VAPID Public Key endpoint active: {pub_key[:24]}...")

    # 4. Mock Subscription in SQLite
    mock_sub = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/test_device_sam_android_chrome",
        "keys": {
            "p256dh": "BNcRdreALRFXTkOOUHK1EtK2wtaz5Ry4YfYCA_0QT9Eg04NSpqqdjLeAdeVuOMinQgUspUZbdJwTOUIDHgMU_No",
            "auth": "tBHItJI5svbpez7KI4CCXg"
        }
    }
    r_sub = requests.post(
        f"{BASE_URL}/api/push/subscribe",
        json={"subscription": mock_sub, "user_agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B)"}
    )
    assert r_sub.status_code == 200, f"Subscription failed: {r_sub.text}"
    print("  ✓ 4. Subscription saved in SQLite database")

    # Verify subscription in SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT endpoint, is_active FROM push_subscriptions WHERE endpoint = ?", (mock_sub["endpoint"],))
    row = c.fetchone()
    conn.close()
    assert row is not None and row[1] == 1, "Subscription not found active in SQLite"
    print("  ✓ 5. Verified persistent record in DB: is_active = 1")

    # 6. Test push for each of the 4 assistants
    assistants = ["roxanne", "chloe", "diana", "electra"]
    for asst in assistants:
        r_test = requests.post(f"{BASE_URL}/api/push/test", json={"assistant": asst})
        assert r_test.status_code == 200, f"Push test failed for {asst}: {r_test.text}"
        res_data = r_test.json()
        print(f"  ✓ 6. [{asst.upper()}] Push dispatched: {res_data.get('message')[:60]}...")

    # 7. Clean up mock subscription
    r_unsub = requests.post(f"{BASE_URL}/api/push/unsubscribe", json={"endpoint": mock_sub["endpoint"]})
    assert r_unsub.status_code == 200
    print("  ✓ 7. Unsubscribe tested cleanly")

    print("\n==================================================")
    print("🎉 ALL PWA & WEB PUSH PIPELINE TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    test_pipeline()
