#!/usr/bin/env python
# encoding: utf-8



# ############################################################################################
#
#   Extracts information of a given movie title
#
# 	Features:
# 	1. Reads movie titles from .csv file
# 	2. Select fields from the information is written into an output .csv file
#
# 	API:
# 	1. OMDb API		(http://www.omdbapi.com/)
#		The OMDb API is a free web service to obtain movie information, all content and images 
#		on the site are contributed and maintained by our users.
#
#   Author: Brahmendra Sravan Kumar Patibandla
# 	Created on: 15-APR-2016
# ############################################################################################



import urllib.request as url_request
import urllib.parse as url_parse
import json
import csv


def encode_url(title, year=''):
    """
    Encodes the title of the movie and year to the format specified by API
    Ex: For extracting information about movie "Frozen" released in 2013
        URL : http://www.omdbapi.com/?t=frozen&y=2013&plot=short&r=json
    :param title: Title of the movie
    :param year: Year of release (Optional)
    :return: Encoded url conforming to the format specified by OMDb API
    """
    url_prefix = "http://www.omdbapi.com/?"
    url_suffix = "&plot=short&r=json"
    title_request = "t=" + url_parse.quote_plus(title.strip())
    year_request = "&y=" + year.strip()
    return url_prefix + title_request + year_request + url_suffix


def get_movie_data(title, year=''):
    """
    Extracts and Return data extracted using API in JSON format
    :param title: Title of the movie
    :param year: Year of release (Optional)
    :return: Data from API in JSON format
    """
    request_url = encode_url(title, year)
    page = url_request.urlopen(request_url)
    content = page.read().decode('utf-8')
    return json.loads(content)


if __name__ == '__main__':
    # Fieldnames which are be extracted from IMDB
    json_field_names = ["Title", "Year"]
    # Input file with movie titles and release year
    input_file = csv.DictReader(open("data/movies_dataset.csv"))
    # Creating an output file to write the results
    # If information about a movie is not found, there would be an empty line in the output file.
    # Hence, results would be in the same order of the input, but blank lines may appear if details of the corresponding movie are unavailable
    result_file = csv.DictWriter(open("data/result_dataSet.csv", 'w', newline=''), fieldnames=json_field_names)
    result_file.writeheader()
    for line in input_file:
        if line['Title'] != '':
            data = get_movie_data(line['Title'], line['Year'])
            filtered_data = {key: value for key, value in data.items() if key in json_field_names}
            result_file.writerow(filtered_data)
