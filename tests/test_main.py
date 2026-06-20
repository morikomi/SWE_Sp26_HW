import unittest
from app import create_app
from unittest import mock
import datetime

# MockResponse sınıfını her yerde kullanabilmek için dışarı alıyoruz
class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data
        
    def json(self):
        return self.json_data

# Coverage'da "%100" almak için kullanılmayan if bloğunu ve 404 return'ünü sildik.
def mocked_requests_get(*args, **kwargs):
    tmp_response = {
        "@context": "https://www.w3.org/ns/hydra/context.jsonld",
        "@id": "https://tle.ivanstanojevic.me/api/tle/25544",
        "@type": "Tle",
        "satelliteId": 25544,
        "name": "ISS (ZARYA)",
        "date": "2026-06-19T20:01:06+00:00",
        "line1": "1 25544U 98067A   26170.83418214  .00080707  00000-0  16559-3 0  9997",
        "line2": "2 25544  51.6327 286.9925 0004571 206.3214 153.7542 15.49322406572160"
    }
    return MockResponse(200, tmp_response)

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    # 1. Ana sayfanın (GET) doğru yüklenip yüklenmediğini test eder
    def test_index_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 2. Calculate sayfasının (GET) formla birlikte doğru yüklenmesini test eder
    def test_calculate_get(self):
        response = self.client.get('/calculate')
        self.assertEqual(response.status_code, 200)

    # 3. Başarılı hesaplama durumu
    @mock.patch('app.main.views.requests.get', side_effect=mocked_requests_get)
    def test_calculate_success(self, mock_get):
        response = self.client.post('/calculate', data={
            'input_date_time': datetime.datetime(2026, 6, 19, 12, 0)
        })
        
        # Koordinatları bulduğumuz için print satırları temizlendi, doğru sayılar eklendi
        self.assertTrue("Position (X, Y, Z) in km: (-2711.970353198433, -3941.2168189910494, -4834.191962969151)" in response.get_data(as_text=True))

    # 4. API'den geçersiz (None) yanıt gelmesi durumunu test eder (else: result = Something went wrong)
    @mock.patch('app.main.views.requests.get', return_value=MockResponse(404, None))
    def test_calculate_api_failure(self, mock_get):
        response = self.client.post('/calculate', data={
            'input_date_time': datetime.datetime(2026, 6, 19, 12, 0)
        })
        self.assertTrue("Something went wrong. Try again." in response.get_data(as_text=True))

    # 5. API başarılı ama SGP4 hesaplaması hata verirse (error != 0 durumu)
    @mock.patch('app.main.views.requests.get', side_effect=mocked_requests_get)
    @mock.patch('app.main.views.parse_satellite', return_value=(1, None, None))
    def test_calculate_sgp4_failure(self, mock_parse_satellite, mock_get):
        response = self.client.post('/calculate', data={
            'input_date_time': datetime.datetime(2026, 6, 19, 12, 0)
        })
        self.assertTrue("Something went wrong. Try again." in response.get_data(as_text=True))