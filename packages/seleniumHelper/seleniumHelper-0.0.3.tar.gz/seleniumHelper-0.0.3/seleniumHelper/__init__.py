from selenium import webdriver

def clickFzg(driver, type, amount = 1):
    try:
        FzgListe = driver.find_elements_by_xpath("//tr[contains(@vehicle_type, '" + type + "')]/td[1]/input")
        for x in range(amount):
            driver.execute_script("arguments[0].scrollIntoView();", FzgListe[x])
            FzgListe[x].click()
        return True
    except:
        print(str(type), "not clickable")
        return False

def print2():
    print("test")
