#String Search Server
 
Overview

The String Search Server is a multithreaded server designed to handle multiple client connections concurrently. It receives a string from a client, searches for this string in a specified file, and responds with either "STRING EXISTS" or "STRING NOT FOUND". The server supports SSL authentication to ensure secure communication.

 Features

- Multithreaded to handle multiple concurrent client connections.
- Supports multiple string search algorithms: Rabin-Karp, KMP, Binary Search.
- Configurable to re-read the file on each query for up-to-date results.
- Can be run as a Linux daemon or service using `systemd`.
- Secure communication using SSL authentication.

Create a Systemd Service File
Create the Service File

Create a new service file for your server, for example, string_search_server.service, in the /etc/systemd/system/ directory:


sudo nano /etc/systemd/system/string_search_server.service
Add the Following Configuration


Description=String Search Server
After=network.target

For the service
User=nobody
Group=no group
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/python /path/to/your/project/server.py --config /path/to/your/project/config.env
Restart=always

Install WantedBy=multi-user.target
Replace /path/to/your/project with the actual path to your project directory and ensure the ExecStart path points to the correct location of your Python virtual environment and server script.

Step 2: Configure Permissions and Reload Systemd
Set Permissions

sudo chmod 644 /etc/systemd/system/string_search_server.service
Reload Systemd


sudo systemctl daemon-reload
Enable the Service


sudo systemctl enable string_search_server.service
Start the Service


sudo systemctl start string_search_server.service
Check the Status

sudo systemctl status string_search_server.service
You should see the service running. Any issues will be logged and can be viewed using:sudo journalctl -u string_search_server.service



 Project Structure

string_search_server/
├── config/
│ └── config.ini
├── src/
│ ├── main.py
│ ├── server.py
│ ├── search_algorithms.py
│ ├── utils.py
├── tests/
│ ├── main.py
│ ├── test_search_algorithms.py
│ ├── test_server.py
├── requirements.txt
├── README.md
└── setup.py
 ├── Report



Setup Instructions
Clone the Repository


git clone <repository_url>
cd <repository_directory>
Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies

pip install -r requirements.txt
Prepare Configuration File
Create a configuration file (e.g., config.env) with the following content:


linuxpath=/path/to/your/200k.txt
reread_on_query=True  # Set to False to keep the file in memory
port=8000  # The port number the server will bind to
use_ssl=True  # Set to False if SSL is not needed
Generate SSL Certificates (if using SSL)
Generate a self-signed certificate and key:

openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
Place server.crt and server.key in the project directory.

Running the Server
Start the Server


python server.py --config config.env
The server will bind to the port specified in the configuration file and start listening for connections.

Connecting to the Server
Use a client script or tool Postman to connect to the server and perform search queries. Example using POST:

 POST -d "search_string=your_search_query" https://localhost:8080/search
Ensure you specify the correct port and use https if SSL is enabled.

Running Tests
Install Testing Dependencies

pip install pytest
Run Unit Tests

Pytest
Server Configuration
The server configuration is defined in the config.env file. Key parameters include:

Linux path: Path to the text file to be searched.
reread on query: Boolean flag indicating whether to re-read the file on each query.
port: Port number for the server to bind to.
use ssl: Boolean flag to enable or disable SSL.
Measuring Performance
The performance of different search algorithms can be measured using the provided utility functions. Update the measure execution time and calculate average time functions in the test_search.py file to measure the execution time of each search function.

Security Considerations
Ensure SSL certificates are properly managed and secured.
Validate and sanitize all input data to prevent injection attacks.
Handle concurrency issues carefully to avoid race conditions and deadlocks.

Conclusion
This project provides a robust, secure, and performant server for string search operations on large text files. By following the setup instructions and leveraging the provided features, you can deploy and test the server in your environment.
