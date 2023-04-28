INSTRUCTIONS ON RESUME PARSER:

The program opens a zip file, parses each individual resume and searches for a degree and a name. Once found, it accesses the google drive where resumes are located using the Google Drive API and searches for the corresponding link. With the name, degree, and link found, the program the writes each value as entries in column 1, 2, and 3 of an excel file. There are two resumes out of the 91 recieved that are not parsable since the text returned by the PyPDF2 library is an empty string. For these cases, I would recommend just writing them at the end of the excel file by hand.

The main part of the program is in PROGRAM.PY. This program imports various libraries as well as the GOOGLE_API_FUNCTS.PY file, which has the functions for authenticating the user and requesting data from the Google Drive Api.

REQUIREMENTS:
Any individual that wants to run this parser will have to first authenticate the request using the quickstart.py file. This file can be excecuted using "python3 quickstart.py". Keep in mind, Right after running this file, you will be prompted to share a google account in order to access your drive file. Contact me (Juan Diego Sanz), so that  I can give you the required permission in the backend. 

IMPORTANT:

KEEP THIS GITHUB PRIVATE AT ALL TIMES. The google drive authentication process requires a credentials.json file. This file contains sensitive information relating to your google drive account. If this file is in the github and said github is public, it might fall in the wrong hands.

NOTE FOR GOOGLE DRIVE SUBMISSIONS:

Please specify to brothers that the file HAS TO BE A PDF, word or docx is not allowed for the PyPDF2 library. Moreover, the pdf can have any name, as long as it ends with " First Last.pdf" (keep in mind the space before FIRST). For example, Jhon Doe -> (Resume_whatever - John Doe.pdf).

