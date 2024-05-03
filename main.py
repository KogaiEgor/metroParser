import json
import logging
from parse_products import get_products_cheese


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('parser.log')
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def create_dict(product):
    temp = {
        "id": product['id'],
        "name": product['name'],
        "url": 'https://online.metro-cc.ru' + product['url'],
        "brand": product['manufacturer']['name']
    }
    if product['stocks'][0]['prices']['is_promo']:
        temp['regular_price'] = product['stocks'][0]['prices']['old_price']
        temp['promo_price'] = product['stocks'][0]['prices']['price']
    else:
        temp['regular_price'] = product['stocks'][0]['prices']['price']
        temp['promo_price'] = None

    return temp

def main():
    result = []
    ids = set()

    spb = [15, 16, 20]
    moscow = [10, 11, 12, 13, 14, 17, 18, 19, 49, 308, 356, 363]

    logger = setup_logger()
    logger.info("Start parsing")

    for i in spb + moscow:
        logger.info(f"Store id {i}")
        from_value = 0
        while True:
            data = get_products_cheese(logger, i, from_value)
            if data is None or data["data"]["category"]["products"] is None:
                break

            logger.debug("Page received")
            products = data["data"]["category"]["products"]

            for product in products:
                if product['id'] in ids:
                    continue
                if product['stocks'][0]['text'] == "Отсутствует":
                    logger.debug(f"{product['name']} is out of stock")
                    continue
                temp = create_dict(product)
                result.append(temp)
                ids.add(temp['id'])
                logger.debug(f"{temp['name']} added")

            if len(products) < 30:
                break
            from_value += 30
        logger.info(f"{len(ids)} products in stock after store parsed")

    logger.info(f"Parsed {len(result)} products")
    logger.info("Parsing ended")

    with open('products.json', 'w', encoding='utf-8') as file:
        json.dump(list(result), file, ensure_ascii=False, indent=4)
        logger.info("Products saved to file")


if __name__ == '__main__':
    main()

