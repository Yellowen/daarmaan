import virtualenv
import textwrap


output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'pip'),
                     'install', 'ipython', 'django', 'vakhshour'])
"""))
f = open('bootstrap.py', 'w').write(output)
