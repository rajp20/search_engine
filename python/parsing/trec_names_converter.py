import csv
import re

def main():
    file_path = '../../dataset/IMDb/imdb-extensive-dataset/IMDb names.csv'

    trec_out = open('../../dataset/TREC_names.txt', 'w')

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            trec_out.write('<DOC>\n')
            trec_out.write('<DOCNO>'+str(re.search(r'\d+', row[0]).group())+'</DOCNO>\n')
            trec_out.write('<name>' + str(row[1]) + '</name>\n')
            trec_out.write('<birth_name>' + str(row[2]) + '</birth_name>\n')
            trec_out.write('<height>' + str(row[3]) + '</height>\n')
            trec_out.write('<bio>' + str(row[4]) + '</bio>\n')
            trec_out.write('<birth_details>' + str(row[5]) + '</birth_details>\n')
            trec_out.write('<birth_year>' + str(row[6]) + '</birth_year>\n')
            trec_out.write('<date_of_birth>' + str(row[7]) + '</date_of_birth>\n')
            trec_out.write('<place_of_birth>' + str(row[8]) + '</place_of_birth>\n')
            trec_out.write('<death_details>' + str(row[9]) + '</death_details>\n')
            trec_out.write('<death_year>' + str(row[10]) + '</death_year>\n')
            trec_out.write('<date_of_death>' + str(row[11]) + '</date_of_death\n')
            trec_out.write('<place_of_death>' + str(row[12]) + '</place_of_death\n')
            trec_out.write('<reason_of_death>' + str(row[13]) + '</reason_of_death\n')
            trec_out.write('<spouses>' + str(row[14]) + '</spouses\n')
            trec_out.write('<divorces>' + str(row[15]) + '</divorces\n')
            trec_out.write('<spouses_with_children>' + str(row[16]) + '</spouses_with_children\n')
            trec_out.write('<children>' + str(row[17]) + '</children\n')
            trec_out.write('<primary_profession>' + str(row[18]) + '</primary_profession\n')
            trec_out.write('<known_for_titles>' + str(row[19]) + '</known_for_titles\n')

        file.close()

    trec_out.close()

if __name__ == '__main__':
    main()