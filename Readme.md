Steps :
1. Create a folder anywhere in your desktop
2. Open the folder and run terminal. For this open terminal and nevigate to the folder or on the file explorer nav bar, type CMD and then press enter.
3. Initialize git
    git init
4. Add the repository link to the git remote.
    git remote add origin https://github.com/tilasmip/pet.git
5. clone the repo
    git clone https://github.com/tilasmip/pet.git
    (or if you have the project write access) 
    git pull origin main 
6. Now nevigate to the folter where manage.py file locates
7. Install the requirements
    python -m pip install -r requirements.txt
8. Build the tables
    python manage.py makemigrations
    python manage.py migrate
9. Run the project on localhost
    python manage.py runserver 8000
10. The apis can be accessed by adding the jsonfile from the link to your postman
    https://api.postman.com/collections/9550962-b7fb5af8-5311-4511-bd01-6b31d78bf65a?access_key=PMAT-01GWC71RW832VNXVFNTZC6MAMC