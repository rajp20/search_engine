from amazon.api import AmazonAPI

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
product = amazon.lookup(ItemId='B00EOE0WKQ')
print(product)
