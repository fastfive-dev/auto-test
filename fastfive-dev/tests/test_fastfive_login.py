"""FastFive Members Login Page Tests."""
import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Page selectors
SELECTORS = {
    "email_input": (By.ID, "inputEmail"),
    "password_input": (By.ID, "inputPassword"),
    "login_button": (By.XPATH, "//button[contains(text(), '로그인')]"),
    "login_button_alt": (By.CSS_SELECTOR, "button.button.fill"),
    "remember_checkbox": (By.CSS_SELECTOR, "input[type='checkbox']"),
}

# SPA wait time
SPA_LOAD_TIME = 8
ELEMENT_WAIT_TIME = 15


def wait_for_spa_load(driver):
    """Wait for SPA to fully render."""
    time.sleep(SPA_LOAD_TIME)


def find_login_button(driver):
    """Find login button using multiple selectors."""
    for selector_name in ["login_button", "login_button_alt"]:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(SELECTORS[selector_name])
            )
            if btn:
                return btn
        except TimeoutException:
            continue

    # Fallback: find any button with '로그인' text
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if "로그인" in btn.text:
            return btn

    raise TimeoutException("Login button not found")


@allure.epic("FastFive Members")
@allure.feature("Login Page")
class TestLoginPageLoad:
    """Test login page loads correctly."""

    @allure.story("Page Load")
    @allure.title("로그인 페이지 로드 확인")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_page_loads(self, driver, base_url):
        """Test that the login page loads successfully."""
        with allure.step("로그인 페이지 접속"):
            driver.get(f"{base_url}/sign-in")
            wait_for_spa_load(driver)

        with allure.step("URL 확인"):
            assert "fastfive" in driver.current_url.lower()

    @allure.story("Page Load")
    @allure.title("페이지 타이틀 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_title(self, driver, base_url):
        """Test the login page has correct title."""
        with allure.step("로그인 페이지 접속"):
            driver.get(f"{base_url}/sign-in")
            wait_for_spa_load(driver)

        with allure.step("타이틀 확인"):
            assert "FASTFIVE" in driver.title


@allure.epic("FastFive Members")
@allure.feature("Login Page")
class TestLoginFormElements:
    """Test login form elements exist."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Navigate to login page before each test."""
        driver.get(f"{base_url}/sign-in")
        wait_for_spa_load(driver)

    @allure.story("Form Elements")
    @allure.title("이메일 입력 필드 존재 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_email_input_exists(self, driver):
        """Test email input field exists."""
        with allure.step("이메일 입력 필드 찾기"):
            email_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(SELECTORS["email_input"])
            )

        with allure.step("필드 속성 확인"):
            assert email_input is not None
            assert email_input.get_attribute("placeholder") == "아이디 (이메일)"

    @allure.story("Form Elements")
    @allure.title("비밀번호 입력 필드 존재 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_password_input_exists(self, driver):
        """Test password input field exists."""
        with allure.step("비밀번호 입력 필드 찾기"):
            password_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(SELECTORS["password_input"])
            )

        with allure.step("필드 속성 확인"):
            assert password_input is not None
            assert password_input.get_attribute("placeholder") == "비밀번호"

    @allure.story("Form Elements")
    @allure.title("로그인 버튼 존재 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_button_exists(self, driver):
        """Test login button exists."""
        with allure.step("로그인 버튼 찾기"):
            login_button = find_login_button(driver)

        with allure.step("버튼 텍스트 확인"):
            assert login_button is not None
            assert "로그인" in login_button.text

    @allure.story("Form Elements")
    @allure.title("환영 메시지 표시 확인")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_contains_welcome_message(self, driver):
        """Test page contains welcome message."""
        with allure.step("페이지 텍스트 확인"):
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "패스트파이브 멤버용 웹사이트에 오신 걸 환영합니다" in body_text


@allure.epic("FastFive Members")
@allure.feature("Login Page")
class TestLoginValidation:
    """Test login form validation."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Navigate to login page before each test."""
        driver.get(f"{base_url}/sign-in")
        wait_for_spa_load(driver)

    @allure.story("Form Validation")
    @allure.title("빈 폼 제출 시 페이지 유지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_form_submission(self, driver):
        """Test that empty form shows validation or stays on page."""
        with allure.step("로그인 버튼 클릭"):
            login_button = find_login_button(driver)
            login_button.click()
            time.sleep(2)

        with allure.step("페이지 유지 확인"):
            assert "/sign-in" in driver.current_url

    @allure.story("Form Validation")
    @allure.title("이메일만 입력 시 페이지 유지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_email_only_submission(self, driver):
        """Test submission with only email filled."""
        with allure.step("이메일 입력"):
            email_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(SELECTORS["email_input"])
            )
            email_input.send_keys("test@example.com")

        with allure.step("로그인 버튼 클릭"):
            login_button = find_login_button(driver)
            login_button.click()
            time.sleep(2)

        with allure.step("페이지 유지 확인"):
            assert "/sign-in" in driver.current_url


@allure.epic("FastFive Members")
@allure.feature("Login Page")
class TestLoginFunctionality:
    """Test actual login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Navigate to login page before each test."""
        driver.get(f"{base_url}/sign-in")
        wait_for_spa_load(driver)

    @allure.story("Login")
    @allure.title("잘못된 자격 증명으로 로그인 실패 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wrong_credentials_stays_on_page(self, driver):
        """Test that wrong credentials keep user on login page."""
        with allure.step("잘못된 이메일 입력"):
            email_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(SELECTORS["email_input"])
            )
            email_input.send_keys("fake@test.com")

        with allure.step("잘못된 비밀번호 입력"):
            password_input = driver.find_element(*SELECTORS["password_input"])
            password_input.send_keys("wrongpassword123")

        with allure.step("로그인 버튼 클릭"):
            login_button = find_login_button(driver)
            login_button.click()
            time.sleep(3)

        with allure.step("로그인 페이지 유지 확인"):
            assert "/sign-in" in driver.current_url

    @allure.story("Login")
    @allure.title("올바른 자격 증명으로 로그인 성공 확인")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.skipif(
        not os.environ.get("TEST_EMAIL") or not os.environ.get("TEST_PASSWORD"),
        reason="TEST_EMAIL and TEST_PASSWORD environment variables required"
    )
    def test_successful_login(self, driver):
        """Test successful login with valid credentials."""
        email = os.environ.get("TEST_EMAIL")
        password = os.environ.get("TEST_PASSWORD")

        with allure.step("이메일 입력"):
            email_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(SELECTORS["email_input"])
            )
            email_input.send_keys(email)

        with allure.step("비밀번호 입력"):
            password_input = driver.find_element(*SELECTORS["password_input"])
            password_input.send_keys(password)

        with allure.step("로그인 버튼 클릭"):
            login_button = find_login_button(driver)
            login_button.click()

        with allure.step("페이지 리다이렉트 확인"):
            WebDriverWait(driver, 15).until(
                lambda d: "/sign-in" not in d.current_url
            )
            assert "/sign-in" not in driver.current_url
