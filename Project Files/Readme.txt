Files:
fake_ssh.py: The honeypot server.
	run: python fake_ssh.py
	It generates IP_logins.txt and logins.txt

LTM.py: The Live Threat Map that parses the IP_logins.txt file.
	python LTM.py
Parser.ipynb: Jupyter notebook file that parses the logs using pandas dataframe for more information.
	jupyter-notebook --allow-root