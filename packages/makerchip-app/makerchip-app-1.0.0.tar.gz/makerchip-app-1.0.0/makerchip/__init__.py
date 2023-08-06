from datetime import datetime, timedelta
import time
import requests
import argparse
import signal
import sys
import native_web_app
import re
import click
import urllib
import os
from pathlib import Path
from shutil import copyfile
import threading
import humanize

class bcolors:
    BACKG = '\033[48:2::45:67:90m'
    WHITE = '\033[38;5;253m '
    BOLDON = '\033[1m'
    BOLDOFF = '\033[2m'
    ENDC = '\033[0m'
    ERASE_END = '\033[K'


def print_status(str):
    print("\r" + bcolors.BACKG + bcolors.WHITE + "%s" %str + \
          bcolors.ENDC +bcolors.ERASE_END, end='', flush=True)


# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


# Represents a Makerchip session.
class MakerchipSession:
    server = ""
    design = ""
    design_content = bytearray()
    interval = 10
    http_session = requests.Session()
    proj_path = ""
    last_sync = datetime.now()
    last_mod = datetime.now()
    autosave_on = False
    quiet = False
    watch = False

    def __init__(self, design, server=None, interval=None, from_url=None, quiet=False):
        self.design = design
        self.quiet = quiet
        if server is None:
            self.server = "https://makerchip.com/"
        else:
            self.server = server

        if interval is None:
            self.interval = 10
        else:
            self.interval = interval

        # Create design file
        if from_url is not None:
            r = requests.get(from_url)
            self.design_content = r.content
            with open(design, 'wb+') as f:
                f.write(r.content)
        else:
            self.design_content = open(design, "rb+").read()

    def auth_pub(self):
        try:
            self.http_session.get('%sauth/pub' % self.server)
        except:
            print_status("Error during authentication!")
            sys.exit(1)

    def create_public_project(self):
        f = open(self.design, "r")
        # Create backup file
        copyfile(self.design, "%s_bak" % self.design)

        data = {
            'source': '%s' % (f.read()),
        }
        try:
            resp = self.http_session.post('%sproject/public/' % self.server, data=data)
            self.proj_path = resp.json()['path']
        except:
            print_status("Error while creating new project on server!")
            sys.exit(1)

    def delete_project(self):
        self.http_session.get('%sproject/public/%s/delete' % (self.server, self.proj_path))

    def get_design(self):
        try:
            resp = self.http_session.get('%sproject/public/%s/contents' % (self.server, self.proj_path))
            return resp.json()['value']
        except:
            print_status("Error while requesting design contents!")
            sys.exit(1)

    def start_autosave(self):
        print_status("Waiting for editor to attach.")
        while not self.is_attached():
            time.sleep(self.interval)
        print_status("Editor attached.")
        self.autosave_on = True
        as_th = threading.Thread(target=self.autosave)
        status_th = threading.Thread(target=self.watch)
        as_th.start()
        status_th.start()
        as_th.join()
        status_th.join()

    def stop_autosave(self):
        self.autosave_on = False

    def stop_watch(self):
        self.watch = False

    def autosave(self):
        while self.autosave_on:
            self.save_in_progress = True
            self.last_sync = datetime.now()
            design = self.get_design().encode('ascii')
            if self.check_conflict():
                print_status("\nThe local file has been modified and resulted in a conflict. Exiting!")
                self.delete_project()
                print_status("Make sure your browser session is closed, your changes will get lost!")
                os._exit(1)
            if self.design_content != design:
                self.design_content = design
                self.last_mod = self.last_sync
            self.save()
            self.save_in_progress = False
            time.sleep(self.interval)
        self.autosave_on = False

    def watch(self):
        self.watch = True
        while self.is_attached() and self.autosave_on == True:
            if not self.quiet:
                now = datetime.now()
                sync = humanize.naturaltime(now - self.last_sync)
                mod = humanize.naturaltime(now - self.last_mod)
                if now - self.last_mod > timedelta(minutes= 10):
                    mod = '\033[38;5;3m' + mod
                elif self.last_mod == self.last_sync:
                    mod = '\033[38;5;11m' + mod
                else:
                    mod = '\033[38;5;43m' + mod
                print_status(bcolors.BOLDON + "Sync: " + bcolors.BOLDOFF + "%s, " % sync + \
                      bcolors.BOLDON + "Mod: " + bcolors.BOLDOFF + \
                      "%s" % mod)
            time.sleep(1)
        self.autosave_on = False

    def check_conflict(self):
        if open(self.design, 'rb').read() == self.design_content:
            return False
        else:
            return True

    def save(self):
        f = open(self.design, "wb")
        f.write(self.design_content)
        f.close()

    def is_attached(self):
        try:
            resp = self.http_session.get('%sproject/public/%s/isAttached' % (self.server, self.proj_path))
            val = resp.json()['isAttached']
            if str(val) == 'True':
                return True
            else:
                return False
        except:
            print_status("Error while requesting project status!")
            sys.exit(1)
        # True

    def url(self):
        return "%ssandbox/public/%s" % (self.server, self.proj_path)


def run():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Run Makerchip as a web application.')
    parser.add_argument('design', type=str, nargs=1, help='Design to be edited.')
    parser.add_argument('--from_url', type=str, help='Initialize design from URL.')
    parser.add_argument('--interval', type=int, help='Autosave interval.')
    parser.add_argument('--server', type=str, help='Makerchip server.')
    parser.add_argument('--quiet', action='store_true', help='Disables the status bar.')
    args = parser.parse_args()

    # ToS check and prompt
    home = Path.home()
    file = "%s/.makerchip_accepted" % home
    if not Path(file).exists():
        # Open the app.
        with suppress_stdout_stderr():
            try:
                native_web_app.open("https://makerchip.com/terms/")
            except Exception:
                print(f"No web browser found. Please open a browser and point it to https://makerchip.com/terms/.")
        if click.confirm('Please review our Terms of Service (opened in a separate window). \
Have you read and do you accept these Terms of Service?', default=False):
            Path(file).touch()
        else:
            print("ToS must be accepted!")
            sys.exit(1)
    Path(file).touch()
    print("You have agreed to our Terms of Service here: https://makerchip.com/terms.")

    # Determine if the provided design is a URL or a local file and act accordingly.
    if re.match("[a-z]+://*", args.design[0]):
        url = "https://www.makerchip.com/sandbox?code_url=%s" % urllib.parse.quote_plus(args.design[0])
        # Open the app.
        try:
            native_web_app.open(url)
        except Exception:
            print(f"No web browser found. Please open a browser and point it to {s.url()}.")
        print(url)
    else:
        # Initialize Makerchip session
        s = MakerchipSession(args.design[0], args.server, args.interval, args.from_url, args.quiet)

        # Autheticate
        s.auth_pub()

        # Create a temporary project on the server
        s.create_public_project()

        # Create a signal handler and register it.
        # Used for deleting the project before exiting.
        def exit_gracefully(signum, frame):
            print_status("Deleting project from server before exiting.")
            s.stop_autosave()
            s.stop_watch()
            s.save()
            s.delete_project()
            # Delete backup file
            if os.path.exists("%s_bak" % args.design[0]):
                os.remove("%s_bak" % args.design[0])
            print_status("Exited! Make sure your browser session is closed, your changes will get lost!\n")
            sys.exit(0)

        signal.signal(signal.SIGINT, exit_gracefully)

        # Open the app.
        with suppress_stdout_stderr():
            try:
                native_web_app.open(s.url())
            except Exception:
                print(f"No web browser found. Please open a browser and point it to {s.url()}.")


        # Run autosave while the browser is running.
        s.start_autosave()

        # Terminate script
        exit_gracefully(None, None)


if __name__ == '__main__':
    run()