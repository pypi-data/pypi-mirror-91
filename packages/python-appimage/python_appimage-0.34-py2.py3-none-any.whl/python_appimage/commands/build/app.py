import json
import glob
import os
import platform
import re
import shutil
import stat
import struct

from ...appimage import build_appimage, cert_file_env_string, tcltk_env_string
from ...utils.compat import decode
from ...utils.deps import PREFIX
from ...utils.fs import copy_file, make_tree, remove_file, remove_tree
from ...utils.log import log
from ...utils.system import system
from ...utils.template import copy_template, load_template
from ...utils.tmp import TemporaryDirectory
from ...utils.url import urlopen, urlretrieve


__all__ = ['execute']


def _unpack_args(args):
    '''Unpack command line arguments
    '''
    return args.appdir, args.name, args.python_version, args.linux_tag,        \
           args.python_tag, args.base_image


_tag_pattern = re.compile('python([^-]+)[-]([^.]+)[.]AppImage')

def execute(appdir, name=None, python_version=None, linux_tag=None,
            python_tag=None, base_image=None):
    '''Build a Python application using a base AppImage
    '''

    if base_image is None:
        # Download releases meta data
        content = urlopen(
            'https://api.github.com/repos/niess/python-appimage/releases')     \
            .read()
        releases = json.loads(content.decode())


        # Fetch the requested Python version or the latest if no specific
        # version was requested
        release, version = None, '0.0'
        for entry in releases:
            tag = entry['tag_name']
            if not tag.startswith('python'):
                continue
            v = tag[6:]
            if python_version is None:
                if v > version:
                    release, version = entry, v
            elif v == python_version:
                version = python_version
                release = entry
                break
        if release is None:
            raise ValueError('could not find base image for Python ' +
                             python_version)
        elif python_version is None:
            python_version = version


        # Check for a suitable image
        if linux_tag is None:
            linux_tag = 'manylinux1_' + platform.machine()

        if python_tag is None:
            v = ''.join(version.split('.'))
            python_tag = 'cp{0:}-cp{0:}'.format(v)
            if version < '3.8':
                python_tag += 'm'

        target_tag = '-'.join((python_tag, linux_tag))

        assets = release['assets']
        for asset in assets:
            match = _tag_pattern.search(asset['name'])
            if str(match.group(2)) == target_tag:
                python_fullversion = str(match.group(1))
                break
        else:
            raise ValueError('Could not find base image for tag ' + target_tag)

        base_image = asset['browser_download_url']
    else:
        match = _tag_pattern.search(base_image)
        if match is None:
            raise ValueError('Invalide base image ' + base_image)
        tag = str(match.group(2))
        python_tag, linux_tag = tag.rsplit('-', 1)
        python_fullversion = str(match.group(1))
        python_version, _ = python_fullversion.rsplit('.', 1)


    # Set the dictionary for template files
    dictionary = {
        'architecture' : platform.machine(),
        'linux-tag' : linux_tag,
        'python-executable' : '${APPDIR}/usr/bin/python' + python_version,
        'python-fullversion' : python_fullversion,
        'python-tag' : python_tag,
        'python-version' : python_version
    }


    # Get the list of requirements
    requirements_list = []
    requirements_path = appdir + '/requirements.txt'
    if os.path.exists(requirements_path):
        with open(requirements_path) as f:
            for line in f:
                line = line.strip()
                if (not line) or line.startswith('#'):
                    continue
                requirements_list.append(line)

    requirements = sorted(os.path.basename(r) for r in requirements_list)
    n = len(requirements)
    if n == 0:
        requirements = ''
    elif n == 1:
        requirements = requirements[0]
    elif n == 2:
        requirements = ' and '.join(requirements)
    else:
        tmp = ', '.join(requirements[:-1])
        requirements = tmp + ' and ' + requirements[-1]
    dictionary['requirements'] = requirements


    # Build the application
    appdir = os.path.realpath(appdir)
    pwd = os.getcwd()
    with TemporaryDirectory() as tmpdir:
        application_name = os.path.basename(appdir)
        application_icon = application_name

        # Extract the base AppImage
        log('EXTRACT', '%s', os.path.basename(base_image))
        if base_image.startswith('http'):
            urlretrieve(base_image, 'base.AppImage')
            os.chmod('base.AppImage', stat.S_IRWXU)
            base_image = './base.AppImage'
        elif not base_image.startswith('/'):
            base_image = os.path.join(pwd, base_image)
        system((base_image, '--appimage-extract'))
        system(('mv', 'squashfs-root', 'AppDir'))


        # Bundle the desktop file
        desktop_path = glob.glob(appdir + '/*.desktop')
        if desktop_path:
            desktop_path = desktop_path[0]
            name = os.path.basename(desktop_path)
            log('BUNDLE', name)

            python = 'python' + python_fullversion
            remove_file('AppDir/{:}.desktop'.format(python))
            remove_file('AppDir/usr/share/applications/{:}.desktop'.format(
                        python))

            relpath = 'usr/share/applications/' + name
            copy_template(desktop_path, 'AppDir/' + relpath, **dictionary)
            os.symlink(relpath, 'AppDir/' + name)

            with open('AppDir/' + relpath) as f:
                for line in f:
                    if line.startswith('Name='):
                        application_name = line[5:].strip()
                    elif line.startswith('Icon='):
                        application_icon = line[5:].strip()


        # Bundle the application icon
        icon_paths = glob.glob('{:}/{:}.*'.format(appdir, application_icon))
        if icon_paths:
            for icon_path in icon_paths:
                ext = os.path.splitext(icon_path)[1]
                if ext in ('.png', '.svg'):
                    break
            else:
                icon_path = None
        else:
            icon_path = None

        if icon_path is not None:
            name = os.path.basename(icon_path)
            log('BUNDLE', name)

            remove_file('AppDir/python.png')
            remove_tree('AppDir/usr/share/icons/hicolor/256x256')

            ext = os.path.splitext(name)[1]
            if ext == '.svg':
                size = 'scalable'
            else:
                with open(icon_path, 'rb') as f:
                    head = f.read(24)
                width, height = struct.unpack('>ii', head[16:24])
                size = '{:}x{:}'.format(width, height)

            relpath = 'usr/share/icons/hicolor/{:}/apps/{:}'.format(size, name)
            destination = 'AppDir/' + relpath
            make_tree(os.path.dirname(destination))
            copy_file(icon_path, destination)
            os.symlink(relpath, 'AppDir/' + name)


        # Bundle any appdata
        meta_path = glob.glob(appdir + '/*.appdata.xml')
        if meta_path:
            meta_path = meta_path[0]
            name = os.path.basename(meta_path)
            log('BUNDLE', name)

            python = 'python' + python_fullversion
            remove_file('AppDir/usr/share/metainfo/{:}.appdata.xml'.format(
                        python))

            relpath = 'usr/share/metainfo/' + name
            copy_template(meta_path, 'AppDir/' + relpath, **dictionary)


        # Bundle the requirements
        if requirements_list:
            deprecation = 'DEPRECATION: Python 2.7 reached the end of its life'
            system(('./AppDir/AppRun', '-m', 'pip', 'install', '-U',
                   '--no-warn-script-location', 'pip'), exclude=deprecation)
            for requirement in requirements_list:
                if requirement.startswith('git+'):
                    url, name = os.path.split(requirement)
                    log('BUNDLE', name + ' from ' + url[4:])
                else:
                    log('BUNDLE', requirement)
                system(('./AppDir/AppRun', '-m', 'pip', 'install', '-U',
                       '--no-warn-script-location', requirement),
                       exclude=(deprecation, '  Running command git clone -q'))


        # Bundle the entry point
        entrypoint_path = glob.glob(appdir + '/entrypoint.*')
        if entrypoint_path:
            entrypoint_path = entrypoint_path[0]
            log('BUNDLE', os.path.basename(entrypoint_path))

            with open(entrypoint_path) as f:
                shebang = f.readline().strip()
            if not shebang.startswith('#!'):
                shebang = '#! /bin/bash'

            entrypoint = load_template(entrypoint_path, **dictionary)
            python_pkg = 'AppDir/opt/python{0:}/lib/python{0:}'.format(
                python_version)
            cert_file = '/opt/_internal/certs.pem'
            if not os.path.exists('AppDir' + cert_file):
                cert_file = None
            dictionary = {'entrypoint': entrypoint,
                          'shebang': shebang,
                          'tcltk-env': tcltk_env_string(python_pkg),
                          'cert-file': cert_file_env_string(cert_file)}
            copy_template(PREFIX + '/data/apprun.sh', 'AppDir/AppRun',
                          **dictionary)


        # Build the new AppImage
        destination = '{:}-{:}.AppImage'.format(application_name,
                                                platform.machine())
        build_appimage(destination=destination)
        shutil.move(destination, os.path.join(pwd, destination))
