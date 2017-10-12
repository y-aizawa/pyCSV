# -*- coding: utf-8 -*-
"""
Modules constants.
"""
CSV_SEP = ','
CSV_ENCODING = 'S-JIS'
CSV_QUOTECHAR = '"'
CSV_LINE_TERMINATOR = '\n'
CSV_EXTENSION = '.csv'

RESULT_COMPLETE = 1
RESULT_ERR = 0
RESULT_ERR_UNEXPECTED = -1

NAME_HEADER_COLUMN_NUMBER = 'headerColumnNumber'
NAME_COLUMN_NUMBER = 'columnNumber'
NAME_COLUMN_NUMBERS = 'columnNumbers'
NAME_COLUMN_NUMBER_FROM = 'columnNumber_From'
NAME_COLUMN_NUMBER_TO = 'columnNumber_To'
NAME_ROW_NUMBER = 'rowNumber'
NAME_ROW_NUMBERS = 'rowNumbers'
NAME_TARGET_COLUMN_NUMBER = 'targetColumnNumber'
NAME_KEY_COLUMN_NUMBERS = 'keyColumnNumbers'

MSG_COMPLETE = 'Complete.'
MSG_ERR_NOT_EXIST_FILE = 'Error : Cannot find the CSV file specified. [{}]'
MSG_ERR_NOT_OPEN_FILE = 'Error : Cannot open the CSV file specified. [{}]'
MSG_ERR_EMPTY_FILE = 'Error : The file specified was empty.'
MSG_ERR_INVALID_FORMAT_FILE = 'Error : Invalid CSV file format.'
MSG_ERR_UNEXPECTED = 'Error : An unexpected error occurred.'

MSG_ERR_INVALID_FORMAT_SOURCE = 'Error : The source was invalid format.'
MSG_ERR_EMPTY_SOURCE = 'Error : The source was empty.'
MSG_ERR_NOT_EXIST_DIRECTORY = 'Error : Cannot find the directory specified. [{}]'
MSG_ERR_INVALID_FILE_NAME_CSV = 'Error : Invalid CSV file name. [{}]'
MSG_ERR_CREATE_FILE = 'Error : Cannot create or save this file. [{}]'
MSG_ERR_NOT_FOUND_HEADER_NAME = 'Error : Cannot find the header specified.[{}]'
MSG_ERR_OUT_OF_RANGE = 'Error : The specified {} was out of range. [{}]'
MSG_ERR_OUT_OF_RANGE_LIST = 'Error : The specified {} in the {} was out of range. [{}]'
MSG_ERR_OUT_OF_RANGE_SAMPLING = 'Error : The samplingRatio must be in range 0 to 1. [{}]'
MSG_ERR_KEY_NOT_FOUND = 'Error : The specified key was not found in the column. [key = {}, targetColumnNumber = {}]'
MSG_ERR_HEADER_NAME_DUPLICATED = 'Error : The specified headerName_To is duplicated. [{}]'
MSG_ERR_DELETE_HEADER_ROW = 'Error : Cannot delete the header row.'

MSG_ERR_ADDNOISE_OVERDIGITS = 'Error : The number of digits of the value must be less than 11. [{}]'