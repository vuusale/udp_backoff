# UDP Backoff

Basic python CLI application for server-client communication over UDP channel that implements backoff strategy.

## Prerequisites
It is required to have Python3 installed in order to run the application. Just go to the [official Python website](https://python.org/) and download the release suitable to your machine. For example, if you have 64-bit Windows operating system, download *Windows x86-64 executable installer*. 

After ensuring that Python3 is set up, follow the below steps:

- Clone the repository into a desired location:
  
      $ git clone https://github.com/vuusale/udp_backoff.git
      
- Install the requirements:
  
      $ pip install -r requirements
  
Now you are ready to run the program. 
  
## Usage
Open 2 terminals: one for server and one for client. Then, run the following command in the first tab in order to create a server:
  
    $ python3 udp_backoff.py server
  
For client setup, run below command in the second terminal:
    
    $ python3 udp_backoff.py client
   
Optionally, you can specify the interface using **--host** or **-H** and the port using **--port** or **-p** options. By default, loopback address and port 9001 are used.

## Scenario
The Spotify regional server warehouse provides music streaming services for billions of clients 24/7. Responding time of the servers depends on client load. That is, clients must wait for response according to the next time schedule:
- ###### First interval: 
  Between 12:00 – 17:00 the maximum waiting time must be 2 seconds
  
- ###### Second Interval: 
  After the 17:00 till the 23:59 the maximum waiting time must be for 4 seconds
  
- ###### Third Interval: 
  After the 23:59 till the 12:00 the waiting time must be 1 second
  
The exponential backoff of these intervals are increased by these factors:
- ###### For the first and third intervals: doubles on each iteration
- ###### For the second interval: triples on each iteration
