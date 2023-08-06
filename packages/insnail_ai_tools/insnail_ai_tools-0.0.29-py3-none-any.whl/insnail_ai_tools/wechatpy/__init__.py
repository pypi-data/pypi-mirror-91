import functools
import inspect

from wechatpy.client import WeChatClient as WeChatClient
from wechatpy.client.base import BaseWeChatClient, _is_api_endpoint
from wechatpy.enterprise import WeChatClient as WechatEnterpriseClient

from insnail_ai_tools.wechatpy.department_child import WeChatDepartmentChild
from insnail_ai_tools.wechatpy.external_contact_child import WeChatExternalContactChild


def inject_client(client_class: BaseWeChatClient):
    """
    对指定client做注入重写的类。
    如果需要使用自定义的api，则需要调用inject方法。
    比如，需要使用enterprise client的自定义方法。则调用  inject_wechat_enterprise_client() 即可
    """
    api_endpoints = inspect.getmembers(client_class, _is_api_endpoint)
    for name, api in api_endpoints:
        api_cls = type(api)
        sub_class = api_cls.__subclasses__()
        if sub_class:
            setattr(client_class, name, sub_class[0](client_class))


# inject_wechat_client = functools.partial(inject_client, WeChatClient)
# inject_wechat_enterprise_client = functools.partial(
#     inject_client, WechatEnterpriseClient
# )
