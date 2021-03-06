__all__ = ["www_status", "irc_status"]

from buildbot.status import html, words
from buildbot.status.web import authz, auth
from config import users

authz_cfg = authz.Authz(
    auth=auth.BasicAuth(users),
    gracefulShutdown=False,
    forceBuild='auth',
    forceAllBuilds='auth',
    pingBuilder='auth',
    stopBuild='auth',
    stopAllBuilds='auth',
    cancelPendingBuild='auth')

www_status = html.WebStatus(http_port=8010, authz=authz_cfg,
                            change_hook_dialects={'github': True})

irc_status = words.IRC(host="irc.freenode.net", nick="p3dbuildbot",
                       channels=["#panda3d-devel"], notify_events={
                           'exception': True,
                           'failureToSuccess': True,
                           'successToFailure': True})

# Fix the stupid github hook... I submitted a patch to buildbot for this.
# This should be fixed in buildbot 0.8.11.
from buildbot.status.web.hooks import github
import change_hook
github.getChanges = change_hook.getChanges
github.process_change = change_hook.process_change
