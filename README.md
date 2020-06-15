Flask Tutorial Here:

main tutorial:
https://www.youtube.com/watch?v=zRwy8gtgJ1A

other flask tutorial:
https://www.youtube.com/watch?v=MwZwr5Tvyxo&t=904s

# Dependencies
had to run this command

sudo apt-get install libmysqlclient-dev

<!-- not used on this tutorial -->
pip install flask-sqlalchemy  


pip3 install flask-mysql
<!-- the tutorial recommended doing  a pip install of flask_mysqldb, but this did't work, so instead
I had to to pip install flask-mysql based on this article. -->
https://stackoverflow.com/questions/50901139/error-during-installation-of-flask-mysqldb-python-3-on-a-mac-os-high-sierra

I had an error with a library, so I had to run this command.
<!-- https://github.com/PyMySQL/mysqlclient-python/issues/14 -->
cp -r /usr/local/mysql/lib/* /usr/local/lib/

<!-- helper for form authentication -->
<!-- https://wtforms.readthedocs.io/en/2.3.x/ -->
<!-- https://flask-wtf.readthedocs.io/en/stable/install.html -->
pip3 install Flask-WTF  <!-- not used? -->
pip3 install WTForms

<!-- library to help hash passwords -->
pip3 install passlib
# Database

followed this instructions:
https://medium.com/employbl/how-to-install-mysql-on-mac-osx-5b266cfab3b6

Note: to use the mysql on terminal, i had to run this command:
export PATH=$PATH:/usr/local/mysql/bin
<!-- the one below work indefinitely instead one time only  -->
echo 'export PATH=$PATH:/usr/local/mysql/bin' >> ~/.bash_profile


to initialize:
mysql -u root -p
password:  rockclimber!

# Running the App
To run the app, go to the folder on the command line and run:
python3 app.py
