# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_rauthman']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.8,<3.0.0', 'ujson>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-rauthman',
    'version': '2.0.0a8.post9',
    'description': 'Rule-based authorization manager worked with nonebot2',
    'long_description': "<!--\n * @Author       : Lancercmd\n * @Date         : 2020-11-17 19:05:26\n * @LastEditors  : Lancercmd\n * @LastEditTime : 2021-01-04 14:48:32\n * @Description  : None\n * @GitHub       : https://github.com/Lancercmd\n-->\n# nonebot_plugin_rauthman\n\n- 基于 [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 功能\n\n- 基于规则的授权管理\n\n## 开始使用\n\n建议使用 poetry\n\n- 通过 poetry 添加到 `nonebot2` 项目的 `pyproject.toml`\n\n``` {.sourceCode .bash}\npoetry add nonebot-plugin-rauthman\n```\n\n- 也可以通过 pip 从 [PyPI](https://pypi.org/project/nonebot-plugin-rauthman/) 安装\n\n``` {.sourceCode .bash}\npip install nonebot-plugin-rauthman\n```\n\n- 在 `nonebot2` 项目中设置 `nonebot.load_plugin()`\n> 当使用 [nb-cli](https://github.com/nonebot/nb-cli) 添加本插件时，该条会被自动添加\n\n``` {.sourceCode .python}\nnonebot.load_plugin('nonebot_plugin_rauthman')\n```\n\n- 参照下文在 `nonebot2` 项目的环境文件 `.env.*` 中添加配置项\n\n## 配置项\n\n- 授权管理信息保存位置（必须）：\n\n  `savedata: str` 保存相对路径，示例意为保存至运行目录下的 `Yuni/savedata` 目录\n\n``` {.sourceCode .bash}\n  savedata = Yuni/savedata\n```\n\n- 授权管理应用策略（可选）：\n\n  `0` 根据可用功能授权，当功能在群聊的可用功能列表内时为可用（默认值）\n\n  `1` 根据功能级别授权，当群聊级别不低于功能所需级别时为可用\n\n``` {.sourceCode .bash}\nauth_policy = 0\n```\n\n- 授权管理指令所需的参数（可选）：\n\n  `auth_command: str` 指令名，默认为 `auth`\n\n  `auth_add: str` 启用功能（根据可用功能授权），默认为 `-a`\n\n  `auth_rm: str` 禁用功能（根据可用功能授权），默认为 `-rm`\n\n  `auth_show: str` 展示群功能状态（根据可用功能授权），默认为 `-s`\n\n  `auth_available: str` 展示全局可用功能（根据可用功能授权），默认为 `-av`\n\n``` {.sourceCode .bash}\nauth_command = auth\nauth_add = -a\nauth_rm = -rm\nauth_show = -s\nauth_available = -av\n```\n\n- 为需要管理的 `on_*` 事件设置规则授权，示例意为将一个 `on_command` 事件划入一个名为 `servicename` 的功能，同时设置功能级别 `1`\n\n``` {.sourceCode .python}\n  from nonebot.plugin import on_command\n  from nonebot_plugin_rauthman import isInService\n\n  command = on_command('cmd', rule=isInService('servicename', 1))\n```\n\n- 这样，群聊必须被启用了该功能，或功能级别高于指定值（取决于当前应用的授权管理应用策略）才会进入事件处理\n\n## 特别感谢\n\n- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 优化建议\n\n如有优化建议请积极提交 Issues 或 Pull requests",
    'author': 'Lancercmd',
    'author_email': 'lancercmd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lancercmd/nonebot_plugin_rauthman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
