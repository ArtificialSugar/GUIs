# Description
This is a personal project that included designing different GUIs and creating an interactive user experience with them.  The majority of the design and implementation was done using Qt Designer, PyQt5, OpenCV and SQlite3. GUI functionality includes an option to login or create a new account.  Once logged in with their credentials a user can access their computer webcam through an embedded video feed.

Depending on the application, more fuctionality could certainly be added.  For example, SQlite3 could be upgraded to a more secure database using MySQL. Something I would like to try in the future is having the video GUI include an option for streaming using RTSP.  

# Installation
Step by step installation instructions are given below and have been tested on Windows 10 and Ubuntu 20.04 operating systems.  

<br />__1.&emsp;Download and extract contents of repository__

<br />Click on the Code button above this repository: 
	
![image](https://user-images.githubusercontent.com/105562075/168448040-769fe2a7-bad5-4bc9-9729-3c83bd9c18a8.png)
	
Select the option to Download ZIP --> download to Desktop: 
	
![image](https://user-images.githubusercontent.com/105562075/168448224-0c8d02ed-7052-444c-9eea-350290745254.png)
	
Extract ZIP to Desktop
	
<br /><br />__2.&emsp;Create virtual environment__
 
<br />Download and install miniconda 3.8:
	
Windows 10: https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Windows-x86_64.exe
	
Ubuntu 20.04: https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh
	
<br />Enter the following commands in your CLI to create and activate a virtual environment:
	
	conda create -n [your env name] python=3.8
		
	conda activate [your env name]

<br /><br />__3.&emsp;Install packages and run program__

<br />Inside the newly created virtual environment navigate to the folder that was extracted in step 1.
	
<br />Install openCV and PyQt5 using pip:
		
	pip install opencv-python
		
	pip install pyqt5
	
Run the program:
		
	python GUI.py

# Instructions
1.&emsp;After completing the installation steps, a sign in GUI should appear on your screen (pictured below). Click the text "Create an account".

2.&emsp;Fill in all input boxes under Login Credentials and Account Details.

3.&emsp;Click the Create Account button. Login credentials and account details are stored in the database file accounts.db.

4.&emsp;Next, click on the text "Return to sign in". Use the newly created login credentials to fill in both input boxes titled Username and Password.

5.&emsp;Click the Continue button.

6.&emsp;Frames per second (FPS) are displayed in the bottom right corner of the video GUI.

7.&emsp;To start a webcam feed click on the button with the play icon.  

8.&emsp;To stop the webcam feed click on the button with the stop icon.

9.&emsp;To end the program, click on the X in the top right corner of any GUI window.

<br />![image](https://user-images.githubusercontent.com/105562075/168449178-4bad69ef-4e4f-44dd-815e-fd102a64a607.png) ![image](https://user-images.githubusercontent.com/105562075/168449219-a196eef8-3830-4c7d-8c50-3ee48997ed75.png)
![image](https://user-images.githubusercontent.com/105562075/168449239-ca75c26a-9c74-4b5e-a8d3-6741cca6533c.png) ![image](https://user-images.githubusercontent.com/105562075/168450384-cba0b4f0-3519-4dba-90f4-851fb186a84b.png)
