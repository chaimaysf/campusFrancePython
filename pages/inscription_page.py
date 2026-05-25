import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InscriptionPage:
    URL = "https://www.campusfrance.org/fr/user/register"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)
        time.sleep(2)
        self._accept_cookies()

    def _accept_cookies(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "tarteaucitronPersonalize2")))
            self.driver.find_element(By.ID, "tarteaucitronPersonalize2").click()
            self.driver.execute_script("var el = document.getElementById('tarteaucitronAlertBig'); if(el) el.remove();")
            time.sleep(1)
        except:
            pass

    def _scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def _js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def _select_selectize(self, wrapper_css, data_value):
        selectize_input = self.driver.find_element(By.CSS_SELECTOR, f"{wrapper_css} .selectize-input")
        self._scroll_into_view(selectize_input)
        time.sleep(0.3)
        self._js_click(selectize_input)
        time.sleep(0.5)
        option = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f".selectize-dropdown-content [data-value='{data_value}']")
        ))
        self._js_click(option)

    def _fill_common_fields(self, client):
        # Email via JS
        email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-form #edit-name")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            email_field, client["email"]
        )
        # Password
        self.driver.find_element(By.ID, "edit-pass-pass1").send_keys(client["password"])
        self.driver.find_element(By.ID, "edit-pass-pass2").send_keys(client["confirmPassword"])

        # Civility
        civility_id = "edit-field-civilite-mr" if client["civility"] == "Mr" else "edit-field-civilite-mme"
        self._js_click(self.driver.find_element(By.ID, civility_id))

        # Nom / Prénom
        self.driver.find_element(By.ID, "edit-field-nom-0-value").send_keys(client["lastName"])
        self.driver.find_element(By.ID, "edit-field-prenom-0-value").send_keys(client["firstName"])

        # Pays résidence
        self._select_selectize("#edit-field-pays-concernes-wrapper", client["countryOfResidenceValue"])

        # Autres champs
        self.driver.find_element(By.ID, "edit-field-nationalite-0-target-id").send_keys(client["nationality"])
        self.driver.find_element(By.ID, "edit-field-code-postal-0-value").send_keys(client["postCode"])
        self.driver.find_element(By.ID, "edit-field-ville-0-value").send_keys(client["city"])
        self.driver.find_element(By.ID, "edit-field-telephone-0-value").send_keys(client["phone"])

    def _accept_communications(self):
        el = self.driver.find_element(By.XPATH, '//*[@id="edit-field-accepte-communications-wrapper"]/div')
        el.click()

    def fill_student_form(self):
        with open("testData/student.json") as f:
            client = json.load(f)
        self._fill_common_fields(client)
        # Profil étudiant
        self._js_click(self.driver.find_element(By.ID, "edit-field-publics-cibles-2"))
        # Domaine + niveau
        self._select_selectize("#edit-field-domaine-etudes-wrapper", client["studyFieldValue"])
        self._select_selectize("#edit-field-niveaux-etude-wrapper", client["studyLevelValue"])
        self._accept_communications()

    def fill_searcher_form(self):
        with open("testData/searcher.json") as f:
            client = json.load(f)
        self._fill_common_fields(client)
        # Profil chercheur via XPath comme en C#
        profil_btn = self.driver.find_element(By.XPATH, '//*[@id="edit-field-publics-cibles"]/div[2]')
        self._scroll_into_view(profil_btn)
        time.sleep(0.3)
        profil_btn.click()
        self._select_selectize("#edit-field-domaine-etudes-wrapper", client["studyFieldValue"])
        self._select_selectize("#edit-field-niveaux-etude-wrapper", client["studyLevelValue"])
        self._accept_communications()

    def fill_institutionnel_form(self):
        with open("testData/admin.json") as f:
            client = json.load(f)
        self._fill_common_fields(client)
        # Profil institutionnel
        profil_btn = self.driver.find_element(By.ID, "edit-field-publics-cibles-4")
        self._scroll_into_view(profil_btn)
        time.sleep(0.3)
        self._js_click(profil_btn)
        self.driver.find_element(By.ID, "edit-field-fonction-0-value").send_keys(client["function"])
        self._select_selectize("#edit-field-type-organisme-wrapper", client["organizationTypeValue"])
        self.driver.find_element(By.ID, "edit-field-nom-organisme-0-value").send_keys(client["organizationName"])
        self._accept_communications()

    def get_submit_button(self):
        btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-form #edit-submit")))
        self._scroll_into_view(btn)
        return btn
