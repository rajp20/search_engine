import csv
import re

def main():
    file_path = '../../dataset/IMDb movies.csv'

    trec_out = open('TREC_movies.trectext', 'a+')
    csv_writer = csv.writer(trec_out)

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            csv_writer.writerow('<DOC>')
            csv_writer.writerow('<DOCNO>'+str(re.search('[0-9]+', row['imdb_title_id']))+'</DOCNO>')
            csv_writer.writerow('<TITLE>'+row['title']+'</TITLE>')
            csv_writer.writerow('<year>' + str(row['year']) + '</year>')

if __name__ == '__main__':
    main()
