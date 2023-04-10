<h2>Note: If you have already cloned the project, do <br/><code>git pull origin main </code></h2> from the project folder.
<h4>Steps :</h4>
<ul>
<li>Create a folder anywhere in your desktop</li>
<li>Open the folder and run terminal. For this open terminal and nevigate to the folder or on the file explorer nav bar, type CMD and then press enter.</li>
<li>Initialize git
    <code>git init</code></li>
<li>Add the repository link to the git remote.
    <code>git remote add origin https://github.com/tilasmip/pet.git</code></li>
<li>clone the repo
    <code>git clone https://github.com/tilasmip/pet.git</code>
    (or if you have the project write access) 
    <code>git pull origin main </code></li>
<li>Now navigate to the folder where manage.py file locates</li>
<li>Install the requirements
    <code>python -m pip install -r requirements.txt</code></li>
<li> Now the requirements have been installed, we are going to make the required directories for the file uploads. We are going to make total of 5 folders with only 3 commands. Type the following commands to make folders.
<br/>
mkdir documents/images/profiles
<br/>
mkdir documents/images/products
<br/>
mkdir documents/images/animals
</li>
<li>Build the tables<br/>
    <code>python manage.py makemigrations</code>
    <code>python manage.py migrate</code></li>
 <li>Before using any admin feature make sure to create a superadmin account. To create a superuser account type <br/>
     <code> python manage.py createsuperuser</code>
     <br>
     Fill the details and admin feature is ready to go
<li>Run the project on localhost
    <code>python manage.py runserver 8000</code></li>
    Visit: <a href="http:localhost:8000/admin">this like</a> to access admin feature.
    <br/>
    <i>Note:
        Before proceeding any client features make sure you create the basic required data for Catebgory, Breeds and products. Inital data for animals is optional but best to fill up some data. 
    </i>
<li>The apis can be accessed by adding the jsonfile from the link to your postman
    https://api.postman.com/collections/9550962-b7fb5af8-5311-4511-bd01-6b31d78bf65a?access_key=PMAT-01GWC71RW832VNXVFNTZC6MAMC</li>
</ul>
