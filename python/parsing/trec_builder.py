import re
import json


def main():
    file = open('../../dataset/movie_reviews/pretty_movie_data.json')
    json_object = json.load(file)
    trec_out = open('../../dataset/TREC_combined.txt', 'w')

    for data in json_object:
        values = json_object[data]
        trec_out.write('<DOC>\n')
        trec_out.write('<DOCNO>' + data + '</DOCNO>\n')
        trec_out.write('<TITLE>' + values['Title'] + '</TITLE>\n')
        trec_out.write('<year>' + values['Year'] + '</year>\n')
        trec_out.write('<date_published>' + values['Date Published'] + '</date_published>\n')
        trec_out.write('<genre>' + values['Genre'] + '</genre>\n')
        trec_out.write('<duration>' + values['Duration'] + '</duration>\n')
        trec_out.write('<country>' + values['Country'] + '</country>\n')
        trec_out.write('<language>' + values['Language'] + '</language>\n')
        trec_out.write('<director>' + values['Director'] + '</director>\n')
        trec_out.write('<writer>' + values['Writer'] + '</writer>\n')
        trec_out.write('<production_company>' + values['Production Company'] + '</production_company>\n')
        trec_out.write('<actors>' + values['Actors'] + '</actors>\n')
        trec_out.write('<description>' + values['Description'] + '</description>\n')
        trec_out.write('<avg_vote>' + values['Avg Vote'] + '</avg_vote>\n')
        trec_out.write('<votes>' + values['Votes'] + '</votes>\n')
        trec_out.write('<budget>' + values['Budget'] + '</budget>\n')
        trec_out.write('<reviews_from_users>' + values['Reviews From Users'] + '</reviews_from_users>\n')
        trec_out.write('<reviews_from_critics>' + values['Reviews From Critics'] + '</reviews_from_critics>\n')
        trec_out.write('<reviews>\n')
        review_num = 1
        for review in values['Reviews']:
            trec_out.write(f'<review_{str(review_num)}>\n')
            trec_out.write('<imbid>' + review['imdbid'] + '</imbid>\n')
            trec_out.write('<asin>' + review['asin'] + '</asin>\n')
            trec_out.write('<overall>' + str(review['overall']) + '</overall>\n')
            trec_out.write('<verified>' + str(review['verified']) + '</verified>\n')
            trec_out.write('<review_time>' + review['reviewTime'] + '</review_time>\n')
            trec_out.write('<reviewer_ID>' + review['reviewerID'] + '</reviewer_ID>\n')
            reviewerName = review['reviewerName'] if 'reviewerName' in review else ''
            trec_out.write('<reviewer_name>' + reviewerName + '</reviewer_name>\n')
            reviewText = review['reviewText'] if 'reviewText' in review else ''
            trec_out.write('<review_text>' + reviewText + '</review_text>\n')
            print(reviewText)
            summary = review['summary'] if 'summary' in review else ''
            trec_out.write('<summary>' + summary + '</summary>\n')
            trec_out.write('<unix_review_time>' + str(review['unixReviewTime']) + '</unix_review_time>\n')
            trec_out.write(f'</review_{str(review_num)}>\n')
            review_num += 1
        trec_out.write('</reviews>\n')
        trec_out.write('</DOC>\n')
    trec_out.close()

    print('Done')


if __name__ == '__main__':
    main()
