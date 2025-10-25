from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# Create your tests here.
class AdminLoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()                 
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Superusuari per als tests
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_admin_login_ok(self):
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        # En aquesta part fem el Login
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # Assert: comprovem que som dins del site admin
        self.selenium.find_element(By.XPATH, "//*[text()='Log out']")

