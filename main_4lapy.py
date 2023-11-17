import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def parser_4lapy_app():
    returned_list = []
    for page_count in range(1, 11):
        # Тут установил такой range потому что в данной категории всего 10 страниц, при неизвестном количестве страниц можно было бы сделать через while
        driver.get(
            f"https://4lapy.ru/catalog/sobaki/korm-sobaki/sukhoy-korm-sobaki/?section_id=166&sort=up-price&page={page_count}")

        items = driver.find_elements(By.CSS_SELECTOR, "div.b-common-item")
        for item in items[:-1]:
            try:
                product_availability = item.find_element(By.CSS_SELECTOR, "span.b-common-item__text").text
            except:
                product_link = item.find_element(By.CSS_SELECTOR, "a.b-common-item__description-wrap").get_attribute("href")

                name = item.find_element(By.CSS_SELECTOR, "span.b-item-name").text

                brand = item.find_element(By.CSS_SELECTOR, "span.span-strong").text

                regular_price = item.find_element(By.CSS_SELECTOR, "span.b-common-item__bottom_current_price").text

                promo_price = item.find_element(By.CSS_SELECTOR, "span.b-common-item__prev-price").text

                product_id = re.search(r'offer=(\d+)', product_link)

                if len(promo_price) == 0:
                    promo_price = "акции на данный товар сейчас нет"
                else:
                    broker = promo_price
                    promo_price = regular_price
                    regular_price = broker

                product_data = {
                    "product_id": product_id.group(1),
                    "name": name,
                    "link": product_link,
                    "regular_price": regular_price,
                    "promo_price": promo_price,
                    "brand": brand
                }
                returned_list.append(product_data)

    json_result = json.dumps(returned_list, ensure_ascii=False)
    return json_result


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    print(parser_4lapy_app())
