###############################################################################
# This file is part of Pyano.                                                 #
#                                                                             #
# Pyano is a web interface for the mixmaster remailer, written for mod_python #
# Copyright (C) 2010  Sean Whitbeck <sean@neush.net>                          #
#                                                                             #
# Pyano is free software: you can redistribute it and/or modify               #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# Pyano is distributed in the hope that it will be useful,                    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

import configparser
import pkgutil
from pathlib import Path


PYANO = "Pyano"
DEFAULT_CONFIG = {
    'mixmaster': '/usr/bin/mixmaster',
    'remailer_addr': '',
    'remailer_mx': 'localhost',
    'mlist2': '',
    'allow_from': '',
    'hist_file': '',
    'hist_window': 15,
    'hist_max_uses': 5,
    'banned_file': '',
    'chain_max_length': 5,
    'max_copies': 5,
    'mail_html': '',
    'news_html': '',
    'block_html': '',
    'mail_form_html': '',
    'news_form_html': '',
    'mail2news': 'mail2news@dizum.com, mail2news@mixmin.net, mail2news@m2n.mixmin.net, mail2news@reece.net.au, mail2news@tioat.net, Post',
    'bad_mail2news': ''
}


# todo: improvement?
class Config:
    pass


class ConfigError(Exception):
    pass


conf = Config()


# todo: get rid of this function
def _get_html(config, conf_name, pkg_name):
    param = config.get(PYANO, conf_name)
    if not param:
        return pkgutil.get_data(__name__, pkg_name)
    else:
        try:
            return open(param).read()
        except IOError:
            raise ConfigError("Error reading " + param + ".")


def parse_config(config_file: Path):
    config = configparser.ConfigParser(defaults=DEFAULT_CONFIG)
    config.add_section(PYANO)
    if config_file.exists():
        with config_file.open() as fd:
            config.read(fd)
    return config


# todo: remove ugliness!
config = parse_config(Path("config.text"))
conf.mixmaster = config.get(PYANO, "mixmaster")
conf.remailer_addr = config.get(PYANO, "remailer_addr")
conf.remailer_mx = config.get(PYANO, "remailer_mx")
conf.mlist2 = config.get(PYANO, "mlist2")
conf.allow_from = config.get(PYANO, "allow_from")
conf.hist_file = config.get(PYANO, "hist_file")
conf.hist_window = config.getint(PYANO, "hist_window")
conf.hist_max_uses = config.getint(PYANO, "hist_max_uses")
conf.banned_file = config.get(PYANO, "banned_file")
conf.chain_max_length = config.getint(PYANO, "chain_max_length")
conf.max_copies = config.getint(PYANO, "max_copies")
conf.mail2news = [
    gateway.strip() for gateway in config.get(PYANO, "mail2news").split(",")
]
conf.bad_mail2news = config.get(PYANO, "bad_mail2news")
# todo: move html code to templates directory
conf.mail_html = _get_html(config, "mail_html", "html/mail.html")
conf.news_html = _get_html(config, "news_html", "html/news.html")
conf.block_html = _get_html(config, "block_html", "html/block.html")
conf.mail_form_html = _get_html(config, "mail_form_html", "html/mail_form.html")
conf.news_form_html = _get_html(config, "news_form_html", "html/news_form.html")
