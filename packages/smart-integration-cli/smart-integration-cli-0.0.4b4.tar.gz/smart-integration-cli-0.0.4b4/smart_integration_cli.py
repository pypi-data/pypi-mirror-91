import os
import click
from time import sleep
from color_print import print

from smart_cli.helpers import find_django_manager
from smart_cli.generators.structure import Structure
from smart_cli.generators.docker_structure import DockerAPPStructure


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', default='project', help='This name of your project')
@click.argument('name', type=click.STRING, default='project', required=True)
@click.option(
    '--auth_type', default='basic', help='Choose type of your project(oauth, basic)'
)
@click.argument('auth_type', type=click.STRING, default='basic', required=True)
@click.option(
    '--methods', default='true', help='add methods application, default - true'
)
@click.argument('methods', type=click.STRING, default='true', required=True)
def init(name, auth_type, methods):
    if auth_type.lower() not in ('basic', 'oauth'):
        print(
            f"{auth_type} invalid integration type, must be on of {['basic', 'oauth']}",
            color='yellow',
            tag='error',
            tag_color='red',
        )
        return None
    if name in os.listdir('.'):
        print(
            f'Project with name - {name} exists in this folder.',
            color='yellow',
            tag='error',
            tag_color='red',
        )
        return None

    struct = Structure(name, auth_type)
    print('~~~ install dependencies ~~~', color='blue', tag='start', tag_color='blue')
    struct.install_dependencies()
    print(
        '~~~ Finish install dependencies ~~~',
        color='green',
        tag='complete',
        tag_color='green',
    )
    print('~~~ django app ~~~', color='blue', tag='start', tag_color='blue')
    sleep(1)
    struct.init_django_app()
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print('~~~ manage applications ~~~', color='blue', tag='start', tag_color='blue')
    sleep(0.5)
    struct.rewrite_basic_files()
    sleep(1.5)
    struct.generate_api_apps_files()
    if methods.lower() == 'true':
        struct.generate_methods_files()
    sleep(1.5)
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print('~~~ template done. ~~~ ', color='green', tag='success', tag_color='green')


@cli.command()
@click.option('--command', default='runserver', help='This name of django command')
@click.argument('command', type=click.STRING, default='runserver', required=True)
def django(command):
    manage = find_django_manager()
    os.system(f"python ./{manage} {command}")


@cli.command()
@click.option('--command', default='tail', help='This name of zappa command')
@click.argument('command', type=click.STRING, default='tail', required=True)
def zappa(command, *params):
    str_params = " ".join(p for p in params)
    os.system(f"zappa {command} {str_params}")


@cli.command()
@click.option('--name', default='project', help='This name of your project')
@click.argument('name', type=click.STRING, default='project', required=True)
@click.option(
    '--auth_type', default='basic', help='Choose type of your project(oauth, basic)'
)
@click.argument('auth_type', type=click.STRING, default='basic', required=True)
def docker_init(name, auth_type):
    if auth_type.lower() not in ('basic', 'oauth'):
        print(
            f"{auth_type} invalid integration type, must be on of {['basic', 'oauth']}",
            color='yellow',
            tag='error',
            tag_color='red',
        )
        return None
    if name in os.listdir('.'):
        print(
            f'Project with name - {name} exists in this folder.',
            color='yellow',
            tag='error',
            tag_color='red',
        )
        return None
    struct = DockerAPPStructure(name, auth_type)
    print('~~~ install dependencies ~~~', color='blue', tag='start', tag_color='blue')
    struct.install_dependencies()
    print(
        '~~~ Finish install dependencies ~~~',
        color='green',
        tag='complete',
        tag_color='green',
    )
    print('~~~ manage docker files ~~~', color='blue', tag='start', tag_color='blue')
    sleep(3)
    struct.generate_docker_folder()
    struct.generate_docker_compose_file()
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print('~~~ django app ~~~', color='blue', tag='start', tag_color='blue')
    sleep(2)
    struct.init_django_app()
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print('~~~ manage settings files ~~~', color='blue', tag='start', tag_color='blue')
    sleep(1.5)
    struct.rewrite_basic_files()
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print(
        '~~~ manage application files ~~~', color='blue', tag='start', tag_color='blue'
    )
    sleep(1.5)
    struct.generate_api_apps_files()
    sleep(1.5)
    struct.generate_methods_files()
    struct.generate_requirements_files()
    print('~~~ Finish ~~~', color='green', tag='complete', tag_color='green')
    print('~~~ template done. ~~~ ', color='green', tag='success', tag_color='green')
