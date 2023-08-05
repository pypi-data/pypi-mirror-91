import sys
from .. import ErsiliaBase


class Versioner(ErsiliaBase):

    def __init__(self, config_json=None):
        ErsiliaBase.__init__(self, config_json=config_json)

    def python_version(self):
        vi = sys.version_info
        return "{0}.{1}".format(vi.major, vi.minor)

    def ersilia_version(self):
        from .. import __version__ as ver
        ver = ver.split(".")
        ver = "{0}.{1}.{2}".format(ver[0], ver[1], ver[2].split("+")[0])
        return ver

    def bentoml_version(self):
        from bentoml import __version__ as ver
        return ver

    def server_docker_name(self, tag=None, as_tuple=False):
        if tag is None:
            tag = self.ersilia_version()
        org = self.cfg.EXT.DOCKERHUB_ORG
        img = self.cfg.ENV.DOCKER.SERVER_BASE_IMAGE
        if as_tuple:
            return org, img, tag
        else:
            name = "{0}/{1}:{2}".format(img, org, tag)
            return name

    def base_conda_name(self, tag=None):
        if tag is None:
            tag = self.ersilia_version()
        env = self.cfg.ENV.CONDA.EOS_BASE_ENV
        name = "{0}-{1}".format(env, tag)
        return name
