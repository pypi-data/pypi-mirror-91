"""pwclip packaging information"""
name = 'pwclip'
provides = ['pwcli', 'pwclip', 'ykclip']
version = '1.7.16'
install_requires = [
    'argcomplete', 'psutil', 'PyYAML', 'py-notifier', 'pywin32 >= 1.0;platform_system=="Windows"', 'win10toast >= 0.9;platform_system=="Windows"']
url = 'https://github.com/d0n/pwclip'
download_url = 'http://deb.janeiskla.de/ubuntu/pool/main/p/pwclip/python3-pwclip_%s-1_all.deb'%version
license = "GPLv3+"
author = 'Leon Pelzer'
description = 'password-manager - temporarily saves passwords to the clipboard'
author_email = 'mail@leonpelzer.de'
classifiers = ['Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: OSI Approved :: ' \
                   'GNU General Public License v3 or later (GPLv3+)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Security',
               'Topic :: Security :: Cryptography',
               'Topic :: Desktop Environment',
               'Topic :: Utilities',
               'Topic :: Desktop Environment']
include_package_data = True
long_description = ''
try:
	with open('docs/description.rst', 'r') as rfh:
		long_description = rfh.read()
except FileNotFoundError:
	pass

entry_points = {
    'console_scripts': ['pwcli = pwclip.__init__:pwcli',
	                    'ykcli = pwclip.__init__:ykcli'],
    'gui_scripts': ['pwclip = pwclip.__init__:pwclip',
                    'ykclip = pwclip.__init__:ykclip']}
package_data = {
    '': ['pwclip/docs/'],
    '': ['pwclip/example']}
data_files=[
    ('share/man/man1', ['pwclip/docs/pwclip.1']),
    ('share/pwclip', [
        'pwclip/example/ca.crt', 'pwclip/example/commands.rst',
        'pwclip/example/ssl.crt', 'pwclip/example/ssl.key',
        'pwclip/example/passwords.yaml'])]
