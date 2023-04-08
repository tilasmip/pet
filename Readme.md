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
<li>Now nevigate to the folter where manage.py file locates</li>
<li>Install the requirements
    <code>python -m pip install -r requirements.txt</code></li>
<li>Build the tables<br/>
    <code>python manage.py makemigrations</code>
    <code>python manage.py migrate</code></li>
 <li>Before using any admin feature make sure to create a superadmin account. To create a sueruser account type <br/>
     <code> python manage.py createsuperuser</code>
     <br>
     Fill the details and admin feature is ready to go
<li>Run the project on localhost
    <code>python manage.py runserver 8000</code></li>
    <a> http:localhost:8000/admin to access admin feature</a>
<li>The apis can be accessed by adding the jsonfile from the link to your postman
    https://api.postman.com/collections/9550962-b7fb5af8-5311-4511-bd01-6b31d78bf65a?access_key=PMAT-01GWC71RW832VNXVFNTZC6MAMC</li>
</ul>
