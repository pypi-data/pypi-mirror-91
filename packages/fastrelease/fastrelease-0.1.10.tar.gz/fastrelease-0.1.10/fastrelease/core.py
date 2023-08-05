# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['GH_HOST', 'find_config', 'FastRelease', 'fastrelease_changelog', 'fastrelease_release', 'fastrelease',
           'bump_version', 'fastrelease_bump_version']

# Cell
from fastcore.imports import *
from fastcore.utils import *
from fastcore.foundation import *
from fastcore.script import *
from ghapi.core import *

from datetime import datetime
from configparser import ConfigParser
import shutil,subprocess

# Cell
GH_HOST = "https://api.github.com"

# Cell
def find_config(cfg_name="settings.ini"):
    cfg_path = Path().absolute()
    while cfg_path != cfg_path.parent and not (cfg_path/cfg_name).exists(): cfg_path = cfg_path.parent
    config_file = cfg_path/cfg_name
    assert config_file.exists(), f"Couldn't find {cfg_name}"
    config = ConfigParser()
    config.read(config_file)
    return config['DEFAULT'],cfg_path

# Cell
def _issue_txt(issue):
    res = '- {} ([#{}]({}))'.format(issue.title.strip(), issue.number, issue.html_url)
    if hasattr(issue, 'pull_request'): res += ', thanks to [@{}]({})'.format(issue.user.login, issue.user.html_url)
    res += '\n'
    if not issue.body: return res
    return res + f"  - {issue.body.strip()}\n"

def _issues_txt(iss, label):
    if not iss: return ''
    res = f"### {label}\n\n"
    return res + '\n'.join(map(_issue_txt, iss))

def _load_json(cfg, k):
    try: return json.loads(cfg[k])
    except json.JSONDecodeError as e: raise Exception(f"Key: `{k}` in .ini file is not a valid JSON string: {e}")

# Cell
class FastRelease:
    def __init__(self, owner=None, repo=None, token=None, **groups):
        "Create CHANGELOG.md from GitHub issues"
        self.cfg,cfg_path = find_config()
        self.changefile = cfg_path/'CHANGELOG.md'
        if not groups:
            default_groups=dict(breaking="Breaking Changes", enhancement="New Features", bug="Bugs Squashed")
            groups=_load_json(self.cfg, 'label_groups') if 'label_groups' in self.cfg else default_groups
        os.chdir(cfg_path)
        owner,repo = owner or self.cfg['user'], repo or self.cfg['lib_name']
        token = ifnone(token, os.getenv('FASTRELEASE_TOKEN',None))
        if not token and Path('token').exists(): token = Path('token').read_text().strip()
        if not token: raise Exception('Failed to find token')
        self.gh = GhApi(owner, repo, token)
        self.groups = groups

    def _issues(self, label):
        return self.gh.issues.list_for_repo(state='closed', sort='created', filter='all', since=self.commit_date, labels=label)
    def _issue_groups(self): return parallel(self._issues, self.groups.keys(), progress=False)

    def changelog(self, debug=False):
        "Create the CHANGELOG.md file, or return the proposed text if `debug` is `True`"
        if not self.changefile.exists(): self.changefile.write_text("# Release notes\n\n<!-- do not remove -->\n")
        marker = '<!-- do not remove -->\n'
        try: self.commit_date = self.gh.repos.get_latest_release().published_at
        except HTTP404NotFoundError: self.commit_date = '2000-01-01T00:00:004Z'
        res = f"\n## {self.cfg['version']}\n"
        issues = self._issue_groups()
        res += '\n'.join(_issues_txt(*o) for o in zip(issues, self.groups.values()))
        if debug: return res
        res = self.changefile.read_text().replace(marker, marker+res+"\n")
        shutil.copy(self.changefile, self.changefile.with_suffix(".bak"))
        self.changefile.write_text(res)
        run(f'git add {self.changefile}')

    def release(self):
        "Tag and create a release in GitHub for the current version"
        ver = self.cfg['version']
        notes = self.latest_notes()
        self.gh.create_release(ver, body=notes)
        return ver

    def latest_notes(self):
        "Latest CHANGELOG entry"
        if not self.changefile.exists(): return ''
        its = re.split(r'^## ', self.changefile.read_text(), flags=re.MULTILINE)
        if not len(its)>0: return ''
        return '\n'.join(its[1].splitlines()[1:]).strip()

# Cell
@call_parse
def fastrelease_changelog(debug:Param("Print info to be added to CHANGELOG, instead of updating file", store_true)=False):
    "Create a CHANGELOG.md file from closed and labeled GitHub issues"
    FastRelease().changelog(debug=debug)

# Cell
@call_parse
def fastrelease_release(token:Param("Optional GitHub token (otherwise `token` file is used)", str)=None):
    "Tag and create a release in GitHub for the current version"
    ver = FastRelease(token=token).release()
    print(f"Released {ver}")

# Cell
@call_parse
def fastrelease(debug:Param("Print info to be added to CHANGELOG, instead of updating file", store_true)=False,
                token:Param("Optional GitHub token (otherwise `token` file is used)", str)=None):
    "Calls `fastrelease_changelog`, lets you edit the result, then pushes to git and calls `fastrelease_release`"
    cfg,cfg_path = find_config()
    FastRelease().changelog()
    if debug: return
    subprocess.run([os.environ.get('EDITOR','nano'), cfg_path/'CHANGELOG.md'])
    if not input("Make release now? (y/n) ").lower().startswith('y'): sys.exit(1)
    run('git commit -am release')
    run('git push')
    ver = FastRelease(token=token).release()
    print(f"Released {ver}")

# Cell
def bump_version(version, part=2):
    version = version.split('.')
    version[part] = str(int(version[part]) + 1)
    for i in range(part+1, 3): version[i] = '0'
    return '.'.join(version)

# Cell
@call_parse
def fastrelease_bump_version(part:Param("Part of version to bump", int)=2):
    "Increment version in `settings.py` by one"
    cfg = Config()
    print(f'Old version: {cfg.version}')
    cfg.d['version'] = bump_version(Config().version, part)
    cfg.save()
    print(f'New version: {cfg.version}')