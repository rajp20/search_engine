
def main():
    file = open('../../dataset/amazon_reviews/movies.txt', "rb")
    file_out = open('../../dataset/amazon_reviews/product_ids.csv', 'w')
    print("Name of the file: ", file.name)
    print('Starting read/write')
    product_ids = set()
    for line in file:
        line_arr = line.decode(errors='ignore').split()
        if len(line_arr) is not 0 :
            if line_arr[0] == 'product/productId:' and line_arr[1] not in product_ids :
                product_ids.add(line_arr[1])
                file_out.write(f'{line_arr[1]}\n')
                print(f'Wrote {line_arr[1]}')
    file.close()
    file_out.close()
    print('Done')
if __name__ == "__main__":
    main()
