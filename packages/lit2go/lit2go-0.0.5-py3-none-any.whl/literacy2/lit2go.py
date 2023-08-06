import argparse
import sys, os, shutil, json, unittest, importlib, requests
from contextlib import contextmanager
from colored import fore, style

from io import StringIO

URL = 'https://code.literacy2.com/api'

LIT2 = 'Literacy2'
API_KEY = 'API-KEY'
API_FILE = 'api.json'
INIT_FILE = '__init__.py'
CONF_DIR = 'Literacy2/__conf__'
CONF_FILE = f'Literacy2/__conf__/{API_FILE}'
CODE_DIR = 'Literacy2/code'
TEMP_DIR = f'{CONF_DIR}/__tmp__'
TEST_PREFIX = 'test_'
TEST_POSTFIX = '_testMethodName'
S_FILE = 'setup_file'
S_DIR = 'setup_dir'
S_MODULE = 'setup_module'
K_APIKEY = 'api_key'
K_MD5KEY = 'md5key'
K_MD5PATH = 'md5path'
K_MD5TEST = 'md5test'
K_NAME = 'name'
K_FAILED = 'failed'
K_PASSED = 'passed'
K_SUCCESS = 'success'
K_CODE = 'code'
K_TITLE = 'title'
K_TESTSUITE = 'test_suite'
MODULE_CACHE = 'cache'

COLOR_TITLE = style.RESET + style.BOLD + fore.BLUE
COLOR_PASSED = style.RESET + fore.DARK_GREEN
COLOR_FAILED = style.RESET + style.BOLD + fore.RED


class Terminal:

    @staticmethod
    @contextmanager
    def mute():
        with open(os.devnull, "w") as muted:
            default_stdout = sys.stdout
            sys.stdout = muted
            try:
                yield
            finally:
                sys.stdout = default_stdout


class FileSystem:

    @staticmethod
    def get_test_setup():
        try:
            cwd = os.getcwd()
            if LIT2 in cwd:
                test_module = MODULE_CACHE
                test_dir = os.path.join(cwd.split(LIT2)[0], TEMP_DIR)
                test_file = f'{test_dir}/{test_module}/{INIT_FILE}'
                return {S_MODULE: test_module, S_DIR: test_dir, S_FILE: test_file}
        except:
            pass
        return None

    @staticmethod
    def config_api():
        try:
            if LIT2 in os.getcwd():
                api_path = os.path.join(os.getcwd().split(LIT2)[0], CONF_FILE)
                with open(api_path, 'r') as api_file:
                    return json.loads(api_file.read())
        except:
            pass

        return {API_KEY: None}

    @staticmethod
    def install(api_key):
        cwd = os.getcwd()
        config_dir = os.path.join(cwd, CONF_DIR)
        code_dir = os.path.join(cwd, CODE_DIR)
        os.makedirs(config_dir)
        os.makedirs(code_dir)
        with open(f'{config_dir}/{API_FILE}', 'w') as config:
            config.write(json.dumps({API_KEY: api_key}))

    @staticmethod
    def config_setup(target_dir):
        sys.path.append(f'{os.getcwd()}/{target_dir}')

    @staticmethod
    def test_setup():
        setup = FileSystem.get_test_setup()
        if setup:
            sys.path.append(os.getcwd())
            if not os.path.exists(setup[S_FILE]):
                os.makedirs(f"{setup[S_DIR]}/{setup[S_MODULE]}")
                with open(setup[S_FILE], 'w') as _:
                    pass

    @staticmethod
    def cleanup():
        setup = FileSystem.get_test_setup()
        if setup:
            shutil.rmtree(setup[S_DIR])


class Messages:
    def __init__(self):
        self.display = []

    def header(self, title):
        self.display.append(f'\n{style.BOLD}{title}\n')

    def step(self, title):
        self.display.append(f'{COLOR_TITLE}{title}')

    def passed(self, step):
        self.display.append(f'{COLOR_PASSED}   + {step}')

    def failed(self, step):
        self.display.append(f'{COLOR_FAILED}   - {step}')

    def error(self, title, error):
        self.display.append(f'{COLOR_TITLE}{title}')
        self.display.append(f'{COLOR_FAILED}   ! ERROR -- {error}')
        self.display.append('\n')

    def fatal(self, error):
        color = style.RESET + style.BOLD + fore.RED
        self.display.append(f'{color}=== ERROR ===')
        self.display.append(f'{error}')

    def newline(self):
        self.display.append('')

    def __str__(self):
        return '\n'.join(self.display)


class Harness:
    def __init__(self, url, api_key):
        self.messages = Messages()
        test_setup = FileSystem.get_test_setup()
        if test_setup:
            self.runnable = True
            self.setup_module = test_setup[S_MODULE]
            self.setup_dir = test_setup[S_DIR]
            self.setup_file = test_setup[S_FILE]

            self.url = url
            self.api_key = api_key
            self.is_continued = True
            self.step_number = 0
        else:
            self.runnable = False
            self.messages.newline()
            self.messages.fatal('Please navigate to the Literacy2 directory')

    def __flag_results(self):
        results = [self.results.failures, self.results.errors]
        for result in results:
            for r in result:
                f_obj = r[0]
                method_name = f_obj.__dict__[TEST_POSTFIX]
                self.failed.append(f'{self.test_name}_{method_name}')
                self.is_continued = False

        for name, t_obj in self.test_module.MainTest.__dict__.items():
            if TEST_PREFIX in name:
                doc = t_obj.__doc__
                name_key = f'{self.test_name}_{name}'
                if name_key in self.failed:
                    self.messages.failed(doc)
                else:
                    self.messages.passed(doc)
                    self.passed.append(name_key)

    def __flag_import(self):
        for name, t_obj in self.test_module.MainTest.__dict__.items():
            if TEST_PREFIX in name:
                name_key = f'{self.test_name}_{name}'
                self.failed.append(name_key)

    def __cache(self, test):
        with open(self.setup_file, 'w') as test_file:
            test_file.truncate(0)
            test_file.write(test[K_CODE])

        sys.path.extend([self.setup_dir])
        sys.argv = [sys.argv[0]]

    def __evaluate(self):
        with Terminal.mute():
            self.runner = unittest.TextTestRunner(stream=StringIO())
            self.test_module = importlib.import_module(self.setup_module)
            importlib.reload(self.test_module)
            try:
                if self.is_continued:
                    self.results = self.runner.run(
                        unittest.makeSuite(self.test_module.MainTest))
            finally:
                open(self.setup_file, 'w').close()

    def _prepare(self, test_case):
        self.failed = []
        self.passed = []

        self.test_name = test_case[K_NAME]
        self.step_number += 1
        self.step_title = f'{self.step_number}. {test_case[K_TITLE]}'

    def _execute(self, test):
        try:
            self.__cache(test)
            self.__evaluate()
            if not self.test_module.err_msg:
                if self.is_continued:
                    self.messages.step(self.step_title)
                    self.__flag_results()
            elif self.is_continued:
                self.is_continued = False
                self.messages.error(self.step_title, self.test_module.err_msg)
                self.__flag_import()
        except Exception as e:
            self.messages.fatal(e)

    def _report(self):
        success = self.is_continued
        if len(self.failed) > 0:
            success = False

        report = {
            K_APIKEY: self.api_key,
            K_MD5KEY: self.md5key,
            K_MD5PATH: self.md5path,
            K_MD5TEST: self.md5test,
            K_NAME: self.test_name,
            K_FAILED: self.failed,
            K_PASSED: self.passed,
            K_SUCCESS: success,
        }

        response = json.loads(requests.post(f'{self.url}/a', json=report).text)
        return response

    def _request(self):
        success = True
        try:
            self.test_url = f'{self.url}/T/'
            payload = {
                K_APIKEY: self.api_key,
            }

            response = json.loads(requests.post(self.test_url, json=payload).text)
            self.test_suite = response[K_TESTSUITE]
            self.md5path = response[K_MD5PATH]
            self.md5key = response[K_MD5KEY]
            self.md5test = response[K_MD5TEST]
            self.title = response[K_TITLE]
            self.messages.header(self.title)
        except Exception as e:
            self.messages.fatal(e)
            success = False
        return success

    def run(self):
        if self.runnable:
            if self._request():
                if self.test_suite is not None:
                    for test_case in self.test_suite:
                        self._prepare(test_case)
                        self._execute(test_case)
                        self._report()
                else:
                    self.messages.fatal(f'No requirements found for "{self.title}"')

        print(self.messages)

    @staticmethod
    def assess(config):
        FileSystem.test_setup()
        Harness(URL, config[API_KEY]).run()
        FileSystem.cleanup()
        print()


def main():
    parser = argparse.ArgumentParser(description='Literacy2 Workbook CLI')
    parser.add_argument('-check', dest='check', action='store_true', help='Check code')
    parser.add_argument('-install', dest='install', type=str, help='Register API key')

    args = parser.parse_args()

    if args.install:
        FileSystem.install(args.install)
    elif args.check:
        Harness.assess(FileSystem.config_api())


if __name__ == '__main__':
    main()
