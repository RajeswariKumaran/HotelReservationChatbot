# HotelReservationChatbot
Chatbot created with open ai using langchain framework. This is the bot created to assist in booking rooms for a fictitious hotel named "Ronitha Inns". Once the following installation instructions are carried out and you run main.py, you can interact with the chatbot until you say "bye" or "goodbye" or "end chat". The information collected for booking room will be stored in reservation.json

# Installation Instructions

Important Pipenv Environment Setup Information
We are going to make use of Pipenv which will help enforce specific versions.
Please use the instructions below to create and configure the Pipenv environment for the HotelReservationChatbot project.
Deprecation warnings about Langchain 0.1.0 and 0.2.0 should be ignored as we are not using these versions!
Python Version
First, you must have the 3.11 version of Python installed:
https://www.python.org/downloads/

Pipenv Installation and Configuration
1. Create a hotelreservation directory on your development machine.
2. In your terminal run pip install pipenv or depending on your environment, pip3 install pipenv
3. Create a file in your hotelreservation project directory called Pipfile
4. Copy paste the following code into that new Pipfile (or drag and drop the file that is present in the code repository into hotelreservation project directory
5. 
[[source]]

url = "https://pypi.org/simple"

verify_ssl = true

name = "pypi"

 
[packages]

langchain = "==0.0.352"

openai = "==0.27.8"

python-dotenv = "==1.0.0"

pyboxen = "*"

 
[dev-packages]
 
[requires]

python_version = "3.11"

 
5. Inside your hotelreservation project directory, run the following command to install your dependencies from the Pipfile:
pipenv install
6. Run the following command to create and enter a new environment:
pipenv shell
After doing this your terminal will now be running commands in this new environment managed by Pipenv.
Once inside this shell, you can run Python commands.
eg:
python main.py
7. If you make any changes to your environment variables or keys, you may find that you need to exit the shell and re-enter using the pipenv shell command.

Deprecation warnings about Langchain 0.1.0 and 0.2.0 should be ignored as we are not using these versions!
 
