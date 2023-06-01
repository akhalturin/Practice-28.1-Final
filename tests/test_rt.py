from time import sleep
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_data import AuthForm, CodeForm
from settings import e_mail, pass_word, num_phone


# TRT-002 (открываем страницу авторизации, создаем скриншот страницы)
def test_check_visual_match(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('pic_001.jpg')


# TRT-005 (проверяем что по умолчанию страница авторизации открывается на вкладке "Телефон")
def test_check_default_phone(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# TRT-006 (проверяем что вкладки на странице авторизации переключаются автоматически при указании
# телефона/почты/логина/лицевого счета)
def test_check_automatic_change_tub(selenium):
    form = AuthForm(selenium)

    # вводим телефон
    form.username.send_keys('+79876543210')
    form.password.send_keys('Qwerty123')
    sleep(5)

    assert form.placeholder.text == 'Мобильный телефон'

    # очищаем поле логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим почту
    form.username.send_keys('test@mail.ru')
    form.password.send_keys('Qwerty123')
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'

    # очищаем поле логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим логин
    form.username.send_keys('test123')
    form.password.send_keys('Qwerty123')
    sleep(5)

    assert form.placeholder.text == 'Логин'

    # очищаем поле логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим лицевой счет
    form.username.send_keys('987654321012')
    form.password.send_keys('Qwerty123')
    sleep(5)

    assert form.placeholder.text == 'Лицевой счёт'


# TRT-007 (авторизация по зарегистрированному номеру телефона)
def test_check_success_auth_phone(selenium):
    form = AuthForm(selenium)

    # вводим телефон и пароль
    form.username.send_keys(num_phone)
    form.password.send_keys(pass_word)
    sleep(5)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TRT-008 (авторизация по незарегистрированному телефону)
def test_check_failure_auth_phone(selenium):
    form = AuthForm(selenium)

    # вводим телефон и пароль
    form.username.send_keys('+71234567890')
    form.password.send_keys('Qwerty123')
    sleep(5)
    form.btn_click()

    message_err = form.driver.find_element(By.ID, 'form-error-message')
    assert message_err.text == 'Неверный логин или пароль'


# TRT-009 (авторизация по зарегистрированной почте)
def test_check_success_auth_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys(e_mail)
    form.password.send_keys(pass_word)
    sleep(5)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TRT-010 (авторизация по незарегистрированной почте)
def test_check_failure_auth_email(selenium):
    form = AuthForm(selenium)

    # вводим почту и пароль
    form.username.send_keys('test321@mail.ru')
    form.password.send_keys('Qwerty123')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TRT-016 (авторизация по одноразовому паролю на номер телефона)
def test_check_one_time_code(selenium):
    form = CodeForm(selenium)

    # ввод телефона
    form.address.send_keys(num_phone)

    # устанавливаем паузу в 30 с для ручного ввода капчи при необходимости
    sleep(30)
    form.get_click()

    otc = form.driver.find_element(By.ID, 'rt-code-0')
    assert otc


# TRT-020 (проверяем форму восстановления доступа)
def test_access_recovery(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# TRT-021 (проверяем форму регистрации)
def test_check_registration_form(selenium):
    form = AuthForm(selenium)

    # нажимаем на кнопку "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


# TRT-022 (проверяем доступность пользовательского соглашения)
def test_check_user_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # нажимаем на кнопку "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    title_page = form.driver.execute_script("return window.document.title")

    assert title_page == 'User agreement'


# TRT-023 (проверяем возможность авторизации через социальную сеть Вконтакте)
def test_check_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'oauth.vk.com'


# TRT-024 (проверяем возможность авторизации через социальную сеть Одноклассники)
def test_check_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'


# TRT-025 (проверяем возможность авторизации через портал mail.ru)
def test_check_auth_mail_ru(selenium):
    form = AuthForm(selenium)
    form.mail_ru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


# TRT-026 (проверяем возможность авторизации через паспорт yandex.ru)
@pytest.mark.xfail(reason='Кнопка авторизации через яндекс не отрабатывает с первого раза')
def test_check_auth_yandex(selenium):
    form = AuthForm(selenium)
    form.yandex_btn.click()
    sleep(3)

    assert form.get_base_url() == 'passport.yandex.ru'