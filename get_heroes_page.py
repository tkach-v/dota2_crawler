# Script that gives html page of all heroes

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = r"C:\my_python\tasks\chromedriver.exe"

driver = Chrome(executable_path=driver_path)
driver.get("https://www.dota2.com/heroes?l=english")

# Чекаємо, поки не знайдеться елемент <body>
wait = WebDriverWait(driver, 10)
body = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rootfooter_RootFooter_H4Gkw")))


html = driver.page_source
print(html)

with open("output.html", "w", encoding="utf-8") as f1:
    f1.write(html)

driver.quit()


