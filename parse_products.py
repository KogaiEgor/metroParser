import requests


def get_products_cheese(logger, store_id, from_value=0):
    cookies = {
        'metroStoreId': str(store_id),
        '_slid_server': '6634a76f0c88bd7ecc06a01e',
        '_slsession': '2B131A8E-8CFF-43D1-9707-6B0F43A4578B',
        'active_order': '1',
        'metro_api_session': '0l0GZoyUuqZGlSoy2KE2bKdEpe9N5ywJmQgjUAnS',
        'metro_user_id': 'cf813e44c92826fb86e0efe803dd6d83',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'metroStoreId=15; _slid_server=6634a76f0c88bd7ecc06a01e; _slsession=2B131A8E-8CFF-43D1-9707-6B0F43A4578B; active_order=1; metro_api_session=0l0GZoyUuqZGlSoy2KE2bKdEpe9N5ywJmQgjUAnS; metro_user_id=cf813e44c92826fb86e0efe803dd6d83',
        'origin': 'https://online.metro-cc.ru',
        'priority': 'u=1, i',
        'referer': 'https://online.metro-cc.ru/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    json_data = {
        'query': "query Query($storeId: Int!, $slug: String!, $attributes:[AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $priceLevelsOnline: Boolean) { category (storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevelsOnline: $priceLevelsOnline) { id name slug id parent_id meta { description h1 title keywords } total prices { max min } pricesFiltered { max min } products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters) { health_warning limited_sale_qty id slug name name_highlight article main_article main_article_slug is_target category_id url images pick_up rating icons { id badge_bg_colors rkn_icon caption image type is_only_for_sales stores caption_settings { colors text } stores sort image_png image_svg description end_date start_date status } manufacturer { id image name } packing { size type pack_factors { instamart } } stocks { value text eshop_availability scale prices_per_unit { old_price offline { price old_price type offline_discount offline_promo } price is_promo levels { count price } online_levels { count price discount } discount } prices { price is_promo old_price offline { old_price price type offline_discount offline_promo } levels { count price } online_levels { count price discount } discount } } } } }",
        'variables': {
            'isShouldFetchOnlyProducts': True,
            'slug': 'syry',
            'storeId': store_id,
            'sort': 'default',
            'size': 30,
            'from': from_value,
            'filters': [
                {
                    'field': 'main_article',
                    'value': '0',
                },
            ],
            'attributes': [],
            'in_stock': False,
            'eshop_order': False,
        },
    }
    url = 'https://api.metro-cc.ru/products-api/graph'
    try:
        response = requests.post(url=url, cookies=cookies, headers=headers, json=json_data)
        response.raise_for_status()
        logger.debug(f"200 received")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("An error occurred during the request: %s", e)
        return None
