from demonhunter import Manager

manager = Manager(host='0.0.0.0', port=8000,
				  pg_host='localhost', pg_user="demonhunter",
				  pg_pass="demonhunter", pg_database="demonhunter")

manager.run_webapp()