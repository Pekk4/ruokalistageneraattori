from invoke import task

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def css_builder(ctx):
    ctx.run("npx tailwindcss -i src/static/css/main.css -o src/static/css/style.css --watch")

@task
def start(ctx):
    ctx.run("cd src && flask run")
