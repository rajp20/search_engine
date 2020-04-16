import csv
import re

def main():
    file_path = '../../dataset/IMDb/imdb-extensive-dataset/IMDb movies.csv'

    trec_out = open('../../dataset/TREC_movies.txt', 'w')

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            trec_out.write('<DOC>\n')
            trec_out.write('<DOCNO>'+str(re.search(r'\d+', row[0]).group())+'</DOCNO>\n')
            trec_out.write('<TITLE>'+row[1]+'</TITLE>\n')
            trec_out.write('<original_title>' + row[2] + '</original_title>\n')
            trec_out.write('<year>' + str(row[3]) + '</year>\n')
            trec_out.write('<date_published>' + str(row[4]) + '</date_published>\n')
            trec_out.write('<genre>' + str(row[5]) + '</genre>\n')
            trec_out.write('<duration>' + str(row[6]) + '</duration>\n')
            trec_out.write('<country>' + str(row[7]) + '</country>\n')
            trec_out.write('<language>' + str(row[8]) + '</language>\n')
            trec_out.write('<director>' + str(row[9]) + '</director>\n')
            trec_out.write('<writer>' + str(row[10]) + '</writer>\n')
            trec_out.write('<production_company>' + str(row[11]) + '</production_company>\n')
            trec_out.write('<actors>' + str(row[12]) + '</actors>\n')
            trec_out.write('<description>' + str(row[13]) + '</description>\n')
            trec_out.write('<avg_vote>' + str(row[14]) + '</avg_vote>\n')
            trec_out.write('<votes>' + str(row[15]) + '</votes>\n')
            trec_out.write('<budget>' + str(row[16]) + '</budget>\n')
            trec_out.write('<reviews_from_users>' + str(row[19]) + '</reviews_from_users>\n')
            trec_out.write('<reviews_from_critics>' + str(row[20]) + '</reviews_from_critics>\n')
            trec_out.write('</DOC>\n')

if __name__ == '__main__':
    main()
