# Define the default target (first target in the Makefile)
dev: logs npm-install tailwind-css venv dev-env dev-database
prod: prod-env configure-nginx

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

# Ask database credentials and generate .env file for development
dev-env:
	@echo "Please provide database credentials to be used:"
	@read -p "Username: " db_username; \
	read -p "Password: " db_password; \
	read -p "Database name: " db_name; \
	echo "DATABASE_URL=postgresql://$$db_username:$$db_password@localhost/$$db_name" > .env; \
	echo "POSTGRES_USER=$$db_username" >> .env; \
	echo "POSTGRES_PASSWORD=$$db_password" >> .env; \
	echo "POSTGRES_DB=$$db_name" >> .env; \

	@echo

	@read -p "Do you want to generate the secret key randomly (y) or provide your own (N)? [y/N]: " generate_random; \
	if [ "$$generate_random" = "y" -o -z "$$generate_random" ]; then \
		app_secret_key=$$(openssl rand -hex 32); \
	else \
		read -p "Application's secret key: " app_secret_key; \
	fi; \
	echo "SECRET_KEY=$$app_secret_key" >> .env; \
	echo "LOGGER_CONFIG_FILE=../config/logging.ini" >> .env; \

	@echo "\nProduction environment variables written in .env file.\n"

# Set up development database
dev-database:
	docker compose -f docker-compose.dev.yml up -d 

# Generate production .env file
prod-env:
	@echo "Please provide database credentials to be used:"
	@read -p "Username: " db_username; \
	read -p "Password: " db_password; \
	read -p "Database name: " db_name; \
	echo "DATABASE_URL=postgresql://$$db_username:$$db_password@generator-db/$$db_name" > .env; \
	echo "POSTGRES_USER=$$db_username" >> .env; \
	echo "POSTGRES_PASSWORD=$$db_password" >> .env; \
	echo "POSTGRES_DB=$$db_name" >> .env; \

	@echo

	@read -p "Do you want to generate the secret key randomly (y) or provide your own (N)? [y/N]: " generate_random; \
	if [ "$$generate_random" = "y" -o -z "$$generate_random" ]; then \
		app_secret_key=$$(openssl rand -hex 32); \
	else \
		read -p "Application's secret key: " app_secret_key; \
	fi; \
	echo "SECRET_KEY=$$app_secret_key" >> .env

	@echo

	@read -p "The port where you want the application be accessible from: [default=8000]: " port; \
	: $${port:=8000}; \
	echo "APP_PORT=$$port" >> .env; \
	echo "LOGGER_CONFIG_FILE=../config/logging.ini" >> .env; \

	@echo "\nProduction environment variables written in .env file.\n"

configure-nginx:
	@read -p "Configure the domain name you want nginx listen to: " DOMAIN_NAME; \
	sed -i 's/<domainname>/'"$$DOMAIN_NAME"'/g' nginx.conf; \
	mkdir certs
