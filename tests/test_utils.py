import unittest
from app import create_app
from app.main.utils import build_query, parse_response, parse_satellite
import datetime

# Mock işlemleri için yardımcı sınıf
class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data
        
    def json(self):
        return self.json_data

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # 1. URL üreticiyi test eder (Mevcut testin)
    def test_build_query(self):
        satellite_id = "000000"
        (query, headers) = build_query(satellite_id)
        self.assertEqual(query, "https://tle.ivanstanojevic.me/api/tle/000000")

    # 2. Parse işleminin geçerli verilerle başarılı olma durumu
    def test_parse_response_success(self):
        mock_data = {
            "satelliteId": 25544,
            "name": "ISS (ZARYA)",
            "line1": "1 25544U...",
            "line2": "2 25544...",
            "date": "2026-06-19T20:01:06+00:00"
        }
        response = MockResponse(200, mock_data)
        result = parse_response(response)
        
        self.assertEqual(result["msg"], "OK")
        self.assertEqual(result["satellite_id"], 25544)
        self.assertEqual(result["date"], "19.06.2026 20:01")

    # 3. API'nin hatalı tarih formatı göndermesi durumu (try/except bloğunun çalışması)
    def test_parse_response_invalid_date_format(self):
        mock_data = {
            "satelliteId": 25544,
            "name": "ISS (ZARYA)",
            "line1": "1 25544U...",
            "line2": "2 25544...",
            "date": "Hatalı-Tarih-Formatı"
        }
        response = MockResponse(200, mock_data)
        result = parse_response(response)
        
        # Except bloğuna düşmeli ve tarihi olduğu gibi bırakmalı
        self.assertEqual(result["date"], "Hatalı-Tarih-Formatı")

    # 4. API'den 200 dışında bir kod gelirse (else: result = None durumu)
    def test_parse_response_failure_status(self):
        response = MockResponse(404, {"error": "Not Found"})
        result = parse_response(response)
        self.assertIsNone(result)

    # 5. Uydunun pozisyon/hız hesaplamasının (SGP4) direkt test edilmesi
    def test_parse_satellite_calculation(self):
        # Gerçek ISS verisi
        tle_dict = {
            "line1": "1 25544U 98067A   26170.83418214  .00080707  00000-0  16559-3 0  9997",
            "line2": "2 25544  51.6327 286.9925 0004571 206.3214 153.7542 15.49322406572160"
        }
        target_date = datetime.datetime(2026, 6, 1, 12, 0)
        
        error, r, v = parse_satellite(tle_dict, target_date)
        
        self.assertEqual(error, 0)
        self.assertIsNotNone(r) # Position array boş olmamalı
        self.assertIsNotNone(v) # Velocity array boş olmamalı
