from amazon.api import AmazonAPI


AMAZON_ACCESS_KEY = "AKIAJT73C4QQWKUT7BMQ"
AMAZON_SECRET_KEY = "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"
AMAZON_ASSOC_TAG = "unityx-20"

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
product = amazon.lookup(ItemId='B00EOE0WKQ')
print(product)
