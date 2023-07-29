# Define the default target (first target in the Makefile)
dev: logs npm-install tailwind-css venv get-credentials

prod: logs prod-deps

# Create the "logs" directory
logs:
	mkdir -p logs

# Run "npm install" to install dependencies
npm-install:
	npm install

# Run the Tailwind CSS build command
tailwind-css:
	npx tailwindcss -i src/static/css/main.css -o src/static/css/style.css

venv:
	python3 -m venv venv
	echo "export FLASK_APP=app.py" >> venv/bin/activate
	echo "export FLASK_ENV=development" >> venv/bin/activate
	@. venv/bin/activate && $(MAKE) dev-deps

dev-deps:
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Virtual environment is activated and dependencies will be installed..."; \
		pip install -r requirements.txt; \
	else \
		echo "Virtual environment is not activated, please activate it before installing dependencies."; \
		exit 1; \
	fi

prod-deps:
	pip install -r requirements

# Ask user for database credentials and generate .env file
get-credentials:
	@echo "Please provide database credentials to be used:"
	@read -p "Username: " db_username; \
	read -p "Password: " db_password; \
	read -p "Database name: " db_name; \
	echo "DATABASE_URL=postgresql://$$db_username:$$db_password@localhost/$$db_name" > .env; \
	echo "Database credentials written to .env file."

	@echo "\nNext, provide values for other environment variables:\n"

	@read -p "Do you want to generate the secret key randomly (y) or provide your own (N)? [y/N]: " generate_random; \
	if [ "$$generate_random" = "y" ]; then \
		app_secret_key=$$(openssl rand -hex 32); \
	else \
		read -p "Application's secret key: " app_secret_key; \
	fi; \
	echo "SECRET_KEY=$$app_secret_key" >> .env

	@read -p "Application's logger config file path [DEFAULT='../config/logging.ini']: " logger_path; \
	: $${logger_path:="../config/logging.ini"}; \
	echo "LOGGER_CONFIG_FILE=$$logger_path" >> .env
