import unittest
import json
import os
from unittest.mock import patch
from FlaskAPI import app, LOG_DIR


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        # Ensure the log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)

    def tearDown(self):
        # Clean up after each test
        for filename in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def test_get_log_not_found(self):
        response = self.app.get("/get_log?id=-1")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Log file not found", response.get_data(as_text=True))

    def test_get_log_permission_error(self):
        log_id = 1
        log_file_path = os.path.join(LOG_DIR, f"{log_id}.log")

        # Create a dummy log file
        with open(log_file_path, "w") as f:
            f.write("Dummy log content")

        # Set file permissions to simulate PermissionError
        os.chmod(log_file_path, 0o000)

        response = self.app.get(f"/get_log?id={log_id}")
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            "Permission denied to read the log file", response.get_data(as_text=True)
        )

        # Restore file permissions to allow cleanup
        os.chmod(log_file_path, 0o666)

    def test_get_log_generic_exception(self):
        log_id = 1
        with patch("builtins.open", side_effect=Exception("Generic error")):
            response = self.app.get(f"/get_log?id={log_id}")
            self.assertEqual(response.status_code, 500)
            self.assertIn(
                "An error occurred while reading the log file",
                response.get_data(as_text=True),
            )

    def test_save_log(self):
        log_data = "[2024-07-19 10:00:00] INFO: System started"
        response = self.app.post("/save_log", data=log_data)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], 1)

    def test_save_multiple_logs(self):
        log_data = "[2024-07-19 10:00:00] INFO: System started"
        response = self.app.post("/save_log", data=log_data)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], 1)

        log_data = "[2024-07-19 10:00:00] INFO: System started"
        response = self.app.post("/save_log", data=log_data)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], 2)

    def test_delete_log(self):
        # Save log
        log_data = "[2024-07-19 10:00:00] INFO: System started"
        response = self.app.post("/save_log", data=log_data)
        response_data = json.loads(response.get_data(as_text=True))
        log_id = response_data["id"]

        # Delete log
        response = self.app.delete("/delete_log", json={"id": log_id})
        self.assertEqual(response.status_code, 200)

        # Ensure log is deleted
        response = self.app.get(f"/get_log?id={log_id}")
        self.assertEqual(response.status_code, 404)

    def test_parse_log(self):
        # Save log
        log_data = (
            "[2024-07-19 10:00:00] INFO: System started\n"
            "[2024-07-19 10:02:00] ERROR: Failed to connect to database\n"
            "[2024-07-19 10:03:00] MEASUREMENT: o2 concentration - 25\n"
            "[2024-07-19 10:03:30] WARNING: Going to o2 alarm\n"
            "[2024-07-19 10:04:00] WARNING: Running low on storage space\n"
            "[2024-07-19 10:05:00] MEASUREMENT: co concentration - 0\n"
            "[2024-07-19 10:06:00] WARNING: Running low on storage space\n"
            "[2024-07-19 10:07:00] MEASUREMENT: o2 concentration - 21\n"
            "[2024-07-19 10:08:30] WARNING: Exiting o2 alarm\n"
            "[2024-07-19 10:09:00] WARNING: Running low on storage space\n"
            "[2024-07-19 10:10:00] MEASUREMENT: co concentration - 0.1\n"
            "[2024-07-19 10:11:00] WARNING: Running low on storage space\n"
        )
        response = self.app.post("/save_log", data=log_data)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        log_id = response_data["id"]

        # Parse log
        response = self.app.post("/parse_log", json={"id": log_id})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response_data["error_count"], 1)
        self.assertEqual(response_data["info_count"], 1)
        self.assertEqual(response_data["measurement_count"], 4)
        self.assertEqual(response_data["alarm_count"], 2)
        self.assertIn("2024-07-19 10:03:30", response_data["alarms"])
        self.assertIn("2024-07-19 10:08:30", response_data["alarms"])
        self.assertIn(
            "Average of gas_type: o2 is 23.00", response_data["measurement averages:"]
        )
        self.assertIn(
            "Average of gas_type: co is 0.05", response_data["measurement averages:"]
        )


if __name__ == "__main__":
    unittest.main()
