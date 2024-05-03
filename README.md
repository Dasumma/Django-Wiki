# Setting Up Django
## Installing Python
•	Install Python 3 (https://www.python.org/downloads/) 
o	Web server created using version 3.11.4.
•	Install pip (Should be included with the Python 3 install)
o	To check try running the “pip” command in command prompt.
•	Install virtualenvwrapper-win:
o	Run the following in Command Prompt:
	Pip install virtualenvwrapper-win.
	mkvirtualenv -r “pip requirements.txt” Django-Wiki
•	“Pip requirements.txt” is in the top-level folder of the project.
•	Copy .env file into folder containing "settings.py"
•	Refresh database and test server:

o	Run the following in Command Prompt in the top level of the project folder:

	Workon Django-Wiki

	Python manage.py makemigrations

	Python manage.py migrate.

	Python manage.py runserver --insecure


 
## Running Server
•	Open Command Prompt in the projects top level directory
•	Run the following commands:
o	Workon Django-Wiki
o	Python manage.py runserver --insecure 
 
## General Use
### Main Wiki	
#### Layout
The base look of the website is a simple menu-based web application. The top of the webpage always has a menu bar with a drop down and a search bar. From here you can get to the Entry Index, Facility Index, and Info Type index. There is also an upload page for uploading new entries and a printer index page for viewing details about all the printers in Enjet Aero. The “Sign In” button brings you to a sign in page that is connected to LDAP, some entries cannot be opened without certain permissions. The search bar located on the top right of the web page allows for quick searching of entries on the site, keywords can be entered for all entries to allow for quicker and more efficient searching.
#### Home Page
The home page contains basic information about the website like all the facilities and information types available to search. It also shows how many entries are on the site at a given time.
#### Entry Index Page
The entry index page is a large list of entries from the entire website.
#### Facility Index Page
The facility index page is a list of facilities from the website, each link brings you to a page that has all the entries relating to the given facility.
Infotype Index Page
The infotype index page is a list of information types from the website, each link brings you to a page that has all the entries relating to the given information type.
#### Printer Index Page
The printer index page brings you to a list of facilities, each link will bring you to that facility’s printer index. Each facility’s printer index gives toner levels and stock quantities for each printer.
#### Sign In Page
The sign in page allows the user to sign in to the website using their LDAP credentials, depending on group membership in the DC. Some entries may not be accessible if they are not part of the necessary groups in the DC.
#### Upload Page
The upload page allows a user to upload a new entry. Topic, facility, infotype, team, and group are simple fields to give the entry some metadata. The summary box is a rich text editor that allows the user to copy and paste most documents into it. The Rich Text Editor is also called WYSIWYG (what you see is what you get) this is because what the user sees when they enter the summary field will display the same on the entry page. The document file allows the user to upload a PDF to the website if they choose to do that instead of or in addition to writing the summary. 
#### Admin Page
### Authentication and Authorization
•	Groups – distinct groups allow for permissions to be set on entries and other pages in the site.
•	Users – each user that signs in will be assigned groups based on their LDAP groups. (Some of these settings can be found in the Django Settings file, i.e., adding more groups from LDAP.)
### AXES
•	Shows log in attempts and failures, by default three tries will lock the account out and will need to be unlocked by an administrator.
•	“Python manage.py axes_reset_username” will need to be run on command prompt.
### WIKI
•	Each tab allows for browsing the current entries in each database table. You can edit/create/delete entries from this area. 
Technical Information
Database Information
•	Main database is db.sqlite3
### Models:
#### Infotype
o	Primary_key (ID)
o	Name (CharField)
#### Facility
o	Primary_key (ID)
o	Name (CharField)
#### Team
o	Primary_key (ID)
o	Team (CharField)
#### Group (Default from Django)
o	https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
#### User (Default from Django)
o	https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
#### Document
o	Primary_key (ID)
o	File (FileField)
#### Keyword
o	Primary_key (ID)
o	Keyword (CharField)
#### Entry
o	Primary_key (ID)
o	Topic (CharField)
o	Infotype (ForeignKey = Infotype)
o	Facility (ForeignKey = Facility)
o	Team (ForeignKey = Team)
o	Group (ForeignKey = Group)
o	Author (ForeignKey = User)
o	Date_published (DateField)
o	Date_modified (DateField)
o	Summary (RichTextUploadingField)
o	Document (ForeignKey = Document)
o	Keywords (ManyToMany = Keyword)
#### PrinterModel
o	Primary_key (ID)
o	Name (CharField)
#### Toner
o	Primary_key (ID)
o	Name (CharField)
o	Model (ForeignKey = PrinterModel)
o	Location (ForeignKey = Facility)
o	Yellow (IntegerField) (stock quantity)
o	Magenta (IntegerField) (stock quantity)
o	Cyan (IntegerField) (stock quantity)
o	Black (IntegerField) (stock quantity)
Printer
o	Primary_key (ID)
o	Name (CharField)
o	IP (CharField)
o	Location (ForeignKey = Facility)
o	Model (ForeignKey = PrinterModel)
### Django Views (Webpage logic)
#### Home	
o	View function for home page
o	Displays information about websites contents. 
o	Corresponding URL: “/Wiki/”
o	Corresponding Template: “/home.html”
#### Entry_detail_view
o	View function for a single entry.
o	Displays information about the current entry using a primary_key.
o	Corresponding URL: “/Wiki/Entries/<int: primary_key>”
o	Corresponding Template: “/entries/entry_detail.html”
#### Facility_detail_view
o	View function for a single facility’s entries.
o	Provides links to all the entries in a facility.
o	Corresponding URL: “/Wiki/facility/<int: Primary_key>”
o	Corresponding Template: “/facility/facility_detail.html”
#### Infotype_detail_view
o	View function for a single information-type’s entries.
o	Provides links to all the entries that relate to a type of information. (software, hardware)
o	Corresponding URL: “/Wiki/infotype/<int: primary_key>”
o	Corresponding Template: “/infotype/infotype_detail.html”
#### Team_detail_view
o	View function for a single team’s entries.
o	Provides links to all the entries that relate to a team. (IT, ERP)
o	Corresponding URL: “/Wiki/team/<int: primary_key>”
o	Corresponding Template: “/team/team_detail.html”
#### Entry_list_view
o	View function for all the entries on the website.
o	Provides links to all the entries on the website.
o	Corresponding URL: “/Wiki/entry/”
o	Corresponding Template: “/entry/entry.html”
#### Facility_list_view
o	View function for all the facilities on the website.
o	Provides links to each facility’s entries page.
o	Corresponding URL: “/Wiki/facility/”
o	Corresponding Template: “/facility/facility.html”
#### Infotype_list_view
o	View function for all the information types on the website.
o	Provides links to each information-types entries page.
o	Corresponding URL: “/Wiki/infotype/”
o	Corresponding Template: “/infotype/infotype.html”
#### Upload_dialog
o	View function for the entry upload dialog
o	Page displays a form that allows the user to upload a new entry to the website.
o	Corresponding URL: “/Wiki/upload/”
o	Corresponding Template: “/upload/upload.html”
#### Edit_dialog
o	View function for the entry edit dialog.
o	Page displays a form that allows the user to edit an existing entry on the website.
o	Corresponding URL: “/Wiki/edit/<int: primary_key>”
o	Corresponding Template: “/upload/upload.html”
#### Search_bar_query
o	View function for searching the website using the search bar.
o	Page displays all entries that relate to the search query, extra filters on page.
o	Corresponding URL: “/Wiki/search?q=<query>”
o	Corresponding Template: “/search/search.html”
#### Pdf_view
o	View function for displaying a PDF.
o	The Page displays a PDF, and it is used frequently in iframes on the entry detail page.
o	Corresponding URL: “/Wiki/documents/<int: primary_key>”
o	Corresponding Template: “/entry/pdf_template.html”
#### Logout_view
o	View function for logging out the user.
o	Logs user out and redirects them back to the home page.
o	Corresponding URL: “Wiki/logout/”
o	Corresponding Template: N/A (redirects to home page)
#### Delete_images
o	View function for deleting unused images on the server.
o	Deletes all unused images that are held in the “/documents/ck_uploads/” folder.
o	Corresponding URL: “Wiki/images/delete/”
o	Corresponding Template: N/A
#### Printer_dca_facility_list
o	View function for seeing all the facilities. 
o	Provides links to all the facilities printer information.
o	Corresponding URL: “Wiki/printer/”
o	Corresponding Template: “Printer/printer_facility.html”
#### Printer_dca_detail_list
o	View function for seeing all the printers from a given parameter.
o	Provides toner levels and stock quantities of a list of printers.
o	Corresponding URL: “Wiki/Printer/<int: primary_key>/”
o	Corresponding Template: “Printer/printer.html”
#### Printer_dca_detail_single
o	View function for seeing the details of a given printer.
o	Provides toner levels and stock quantities of one printer. Usually used in an iframe.
o	Corresponding URL: “Wiki/printer_detail/<int: primary_key>/”
o	Corresponding Template: “printer/printer_detail.html”
#### Printer_edit_toner
o	View function for editing toner stocks
o	View and change toner stocks for specific model of printer in a facility.
o	Corresponding URL: “Wiki/edittoner/<int: primary_key>/”
o	Corresponding Template: “upload/upload_toner.html”
#### Custom_404
o	View for custom 404 error display
#### Custom_500
o	View for custom 500 error display
