import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

BASE_URL = 'https://alsanafer.ps/?app=product.cat.59&size='

def scrape_data(size):
    try:
        # Make a request to the page
        response = requests.get(f"{BASE_URL}{size}")

        if response.status_code != 200:
            raise Exception(f"Failed to load page with status code {response.status_code}")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find product elements
        product_elements = soup.select('.product-brief-content-wrapper')

        products = []
        for element in product_elements:
            if 'out-of-stock' in element.get('class', []):
                continue

            name = element.select_one('.product-brief-content .flex-row .title')
            price_text = element.select_one('.product-brief-content .flex-row .price')
            image = element.select_one('.product-brief-content .flex-row .image-wrapper img')

            # Extract the data if available
            if name and price_text and image:
                name = name.get_text(strip=True)
                price_text = price_text.get_text(strip=True)
                price = int(price_text.replace('₪', '').strip()) + 20
                image_url = image.get('src')

                full_image_url = f'https://alsanafer.ps/{image_url.strip()}' if image_url else None

                if name and price is not None and full_image_url:
                    products.append({
                        'name': name,
                        'price': price,
                        'image': full_image_url
                    })

        return products
    except Exception as e:
        print(f"Error scraping data: {e}")
        return []

# Django view
def scrape_data_view(request, size=2):
    products = scrape_data(size)
    sizes = list(range(2, 19, 2))
    return render(request, 'template.html', {'products': products, 'selected_size': size ,'sizes':sizes})
