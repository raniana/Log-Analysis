## Log Analysis:

This code is a log analysis tool, Analyze data collected from a website logs and displays statistical data about the content.

## How to Run The Code:

**Python 2.7 or 3 and Oracle VM virtualBox** should be installed on your computer. First the database should be setup and populated with data.
 Download the file newsdata.sql and put it into the vagrant directory, which is shared with your virtual machine. To load the data Cd into the vagrant directory and run the command: 
                    
                  psql -d news -f newsdata.sql 

This command will create tables and populate them with data inside a database called news. Then Copy and paste the log_analysis.py file inside the vagrant directory. Cd to the vagrant
directory and type  :

python filename.py

The code will run inside the virtual machine on your computer and disply the results on the terminal screen.
