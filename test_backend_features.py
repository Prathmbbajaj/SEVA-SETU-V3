"""
Verification test suite for backend API endpoints:
- Mandatory Proof of Work on job completion (400 if proof missing, 200 with proof)
- Customer Service History
- Worker Service History
- Driver Telemetry Stream
- 24x7 Worker Escalation
- Emergency Helpline Call Logging
- Customer Driver Crime & Misconduct Reporting (112 Police Dispatch)
- Strict OTP Verification: START_OTP can ONLY be verified after job is ACCEPTED by worker
"""

import sys
from pathlib import Path

backend_dir = str(Path(__file__).parent / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import unittest
from fastapi.testclient import TestClient
from backend.main import app
import dispatch

client = TestClient(app)

class TestNewBackendFeatures(unittest.TestCase):

    def test_01_mandatory_proof_of_work(self):
        # Seed a test booking in IN_PROGRESS state
        booking_id = 9999
        dispatch.BOOKINGS_DB[booking_id] = {
            "booking_id": booking_id,
            "service_type": "driver",
            "worker_id": 104,
            "customer_name": "Aarav Mehta",
            "end_otp": "7788",
            "status": "IN_PROGRESS",
            "pricing": {"cooperative_wage_payout": 500.0},
            "timeline": ["Service commenced"]
        }

        # 1. Attempt completion WITHOUT proof image -> Must return HTTP 400
        res_fail = client.post("/api/service/complete-with-proof", json={
            "booking_id": booking_id,
            "worker_id": 104,
            "end_otp": "7788",
            "proof_image": "",
            "work_notes": "Attempt without proof",
            "odometer_reading": "24,842 km"
        })
        self.assertEqual(res_fail.status_code, 400, "Should reject completion without proof image")
        self.assertIn("mandatory", res_fail.json().get("detail", "").lower())

        # 2. Complete WITH valid proof photo -> Must succeed with HTTP 200
        res_ok = client.post("/api/service/complete-with-proof", json={
            "booking_id": booking_id,
            "worker_id": 104,
            "end_otp": "7788",
            "proof_image": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d",
            "work_notes": "Trip concluded safely, odometer checked.",
            "odometer_reading": "24,842 km"
        })
        self.assertEqual(res_ok.status_code, 200, "Should complete job when proof is provided")
        data = res_ok.json()
        self.assertEqual(data.get("status"), "COMPLETED")
        self.assertTrue(data.get("booking", {}).get("proof_of_work", {}).get("verified"))

    def test_02_customer_and_worker_history(self):
        res_cust = client.get("/api/history/customer/Aarav%20Mehta")
        self.assertEqual(res_cust.status_code, 200)
        cust_history = res_cust.json().get("history", [])
        self.assertTrue(len(cust_history) >= 1)

        res_worker = client.get("/api/history/worker/104")
        self.assertEqual(res_worker.status_code, 200)
        worker_history = res_worker.json().get("history", [])
        self.assertTrue(len(worker_history) >= 1)

    def test_03_driver_telemetry(self):
        # Post telemetry update with required schema fields
        res_post = client.post("/api/driver/telemetry/9999", json={
            "booking_id": 9999,
            "lat": 28.6320,
            "lng": 77.2180,
            "speed_kmh": 46.5,
            "heading_deg": 82.0,
            "distance_traveled_km": 5.4
        })
        self.assertEqual(res_post.status_code, 200)

        # Get telemetry update
        res_get = client.get("/api/driver/telemetry/9999")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json().get("telemetry", {}).get("speed_kmh"), 46.5)

    def test_04_worker_escalation(self):
        res_esc = client.post("/api/worker/escalate", json={
            "worker_id": 104,
            "worker_name": "Vikram Singh",
            "customer_name": "Test Client",
            "customer_phone": "+91 99999 88888",
            "category": "SAFETY_PROTOCOL_VIOLATION",
            "priority": "HIGH",
            "description": "24x7 safety escalation test",
            "delay_hours": 1.5
        })
        self.assertEqual(res_esc.status_code, 200)
        self.assertIn("WRK-ESC-", res_esc.json().get("ticket_id", ""))

    def test_05_emergency_helpline_call(self):
        res_call = client.post("/api/emergency/helpline-call", json={
            "customer_name": "Aarav Mehta",
            "lat": 28.6315,
            "lng": 77.2167,
            "driver_name": "Vikram Singh",
            "vehicle_number": "DL-1Z-9021",
            "speed_kmh": 42.0,
            "emergency_type": "FEMALE_SAFETY_POLICE_SOS",
            "notes": "Simulated emergency helpline test demonstration"
        })
        self.assertEqual(res_call.status_code, 200)
        self.assertIn("SOS-112-", res_call.json().get("call_id", ""))

    def test_06_customer_driver_crime_report(self):
        res_crime = client.post("/api/customer/driver/report-crime", json={
            "booking_id": 8888,
            "customer_name": "Pooja Sharma",
            "customer_phone": "+91 98765 11223",
            "driver_name": "Vikram Singh",
            "driver_id": 104,
            "vehicle_number": "DL-1Z-9021",
            "category": "CRIME_HARASSMENT",
            "priority": "CRITICAL",
            "description": "Driver made vulgar remarks, deviated from route, and refused to stop.",
            "lat": 28.6340,
            "lng": 77.2210,
            "speed_kmh": 48.0,
            "call_helpline_now": True
        })
        self.assertEqual(res_crime.status_code, 200)
        data = res_crime.json()
        self.assertTrue(data.get("success"))
        self.assertIn("POLICE-CRIME-", data.get("ticket_id", ""))
        self.assertTrue(data.get("record", {}).get("pcr_van_dispatched"))

        # Verify driver is suspended
        worker = next((w for w in dispatch.WORKERS if w["id"] == 104), None)
        self.assertIsNotNone(worker)
        self.assertEqual(worker["disciplinary_status"], "SUSPENDED_POLICE_INQUIRY")
        self.assertFalse(worker["is_available"])

    def test_07_strict_otp_fill_lock_until_accepted(self):
        # 1. Seed a booking that is currently BROADCASTING (not yet accepted by worker)
        booking_id = 7777
        dispatch.BOOKINGS_DB[booking_id] = {
            "booking_id": booking_id,
            "service_type": "driver",
            "assigned_worker": {"id": 105, "name": "Mohan Lal"},
            "customer_name": "Kavita Rao",
            "customer_lat": 28.6328,
            "customer_lng": 77.2197,
            "start_otp": "4321",
            "end_otp": "8765",
            "status": "BROADCASTING",
            "timeline": ["Broadcasted to worker"]
        }

        # Attempt to verify START_OTP while still in BROADCASTING status -> Must be rejected
        res_premature = dispatch.verify_start_otp(booking_id, "4321")
        self.assertFalse(res_premature["success"])
        self.assertIn("ACCEPTED by worker first", res_premature["message"])

        # 2. Worker now accepts the job
        accept_res = dispatch.worker_respond_to_job(booking_id, 105, accept=True)
        self.assertTrue(accept_res["success"])
        self.assertEqual(dispatch.BOOKINGS_DB[booking_id]["status"], "ACCEPTED")

        # 3. Now verify START_OTP -> Must succeed
        res_accepted = dispatch.verify_start_otp(booking_id, "4321")
        self.assertTrue(res_accepted["success"])
        self.assertEqual(res_accepted["status"], "IN_PROGRESS")
        self.assertEqual(dispatch.BOOKINGS_DB[booking_id]["status"], "IN_PROGRESS")

if __name__ == "__main__":
    unittest.main()
