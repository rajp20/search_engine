import csv
import re
import json

def main():
    file_path = '../../dataset/movie_reviews/movie_reviews.json'

    trec_out = open('../../dataset/TREC_reviews.txt', 'w')

    with open(file_path, 'r') as file:
        review_dict = {}
        for line in file:
            data = json.loads(line)
            if data['imdbid'] in review_dict:
                review_dict[data['imdbid']] += 1
            else :
                review_dict[data['imdbid']] = 1
            print(data)
            trec_out.write('<DOC>\n')
            trec_out.write('<DOCNO>' + data['imdbid'] + '_' + str(review_dict[data['imdbid']]) + '</DOCNO>\n')
            trec_out.write('<TITLE>' + data['title'] + '</TITLE>\n')
            trec_out.write('<imbid>' + data['imdbid'] + '</imbid>\n')
            trec_out.write('<asin>' + data['asin'] + '</asin>\n')
            trec_out.write('<overall>' + str(data['overall']) + '</overall>\n')
            trec_out.write('<verified>' + str(data['verified']) + '</verified>\n')
            trec_out.write('<review_time>' + data['reviewTime'] + '</review_time>\n')
            trec_out.write('<reviewer_ID>' + data['reviewerID'] + '</reviewer_ID>\n')
            reviewerName = data['reviewerName'] if 'reviewerName' in data else ''
            trec_out.write('<reviewer_name>' + reviewerName + '</reviewer_name>\n')
            reviewText = data['reviewText'] if 'reviewText' in data else ''
            trec_out.write('<review_text>' + reviewText + '</review_text>\n')
            summary = data['summary'] if 'summary' in data else ''
            trec_out.write('<summary>' + summary + '</summary>\n')
            trec_out.write('<unix_review_time>' + str(data['unixReviewTime']) + '</unix_review_time>\n')
            trec_out.write('</DOC>\n')
        file.close()

    trec_out.close()

if __name__ == '__main__':
    main()