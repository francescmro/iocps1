from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import requests
# Create your tests here.
class AdminLoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()                 
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Superusuari per als tests segons enunciat
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
        # Fem el Login
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # Assert: comprovem que som dins del site admin
        self.selenium.find_element(By.XPATH, "//*[text()='Log out']")

class ViewSiteButtonTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # superusuari per al test segons enunciat
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_staff = True
        user.is_superuser = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_part_personalitzada(self):
        # 1) Login a /admin
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # 2) Busquem al site l'enllaç "View site"
        link = WebDriverWait(self.selenium, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(., 'View site')]"))
            )

        # 3) Comprovem que porta a una URL vàlida (200)
        href = link.get_attribute("href") or "/"
        full_url = href if href.startswith("http") else urljoin(self.live_server_url, href)

        resp = requests.get(full_url, timeout=5)
        assert resp.status_code == 200, f"Status OK"
