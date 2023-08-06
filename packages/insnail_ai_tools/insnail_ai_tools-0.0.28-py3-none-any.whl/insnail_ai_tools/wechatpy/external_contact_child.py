import time

from optionaldict import optionaldict
from wechatpy.enterprise.client.api import WeChatExternalContact


class WeChatExternalContactChild(WeChatExternalContact):
    """
    客户联系人扩展类
    """

    def get_external_group_list(
        self, userid_list: list, status_filter: int = 0, limit: int = 100
    ) -> list:
        """
         获取客户群列表
        https://work.weixin.qq.com/api/doc/90000/90135/92120

        :param userid_list: 企业员工userid标识列表
        :param status_filter: 客户群跟进状态过滤。0 - 所有列表(即不过滤), 1 - 离职待继承, 2 - 离职继承中, 3 - 离职继承完成，默认0
        :param limit: 分页，预期请求的数据量，取值范围 limit: 1~ 1000，默认100
        :return: []
        """
        cursor = ""
        group_chat_list = []
        # owner_filter: 群主userid过滤
        #     userid_list: 企业微信员工userid列表
        # cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用不填
        data = optionaldict(
            status_filter=status_filter,
            owner_filter={"userid_list": userid_list},
            cursor=cursor,
            limit=limit,
        )
        try:
            while True:
                response = self._post("externalcontact/groupchat/list", data=data)
                if (response["errcode"] == 0) and response.get("cursor"):
                    data["cursor"] = response.get("cursor")
                    group_chat_list.extend(response.get("group_chat_list"))
                else:
                    break
            return group_chat_list
        except Exception as e:
            print(e)
            return []

    def get_external_group_statistic_data_by_userid(
        self, userid_list: list, start_time: int = None, end_time: int = None
    ) -> list:
        """
         获取userid为群主的「群聊数据统计」数据
        https://work.weixin.qq.com/api/doc/90000/90135/92133

        :param userid_list: 企业员工userid标识列表
        :param start_time: 数据开始时间；开始时间与结束时间只传一个，默认获取传入时间当天的数据，如果两个都没有传，默认获取昨天的数据
        :param end_time: 数据结束时间
        :return: []
        """
        try:
            external_behavior_list = []
            offset = 0
            # owner_filter: 群主userid过滤，如果不填，表示获取全部群主的数据
            #     userid_list: 企业微信员工userid列表，最多100个
            parameter = {"owner_filter": {"userid_list": userid_list}, "offset": offset}
            if start_time and end_time:
                parameter["day_begin_time"] = start_time
                parameter["day_end_time"] = end_time
            elif start_time:
                parameter["day_begin_time"] = start_time
            elif end_time:
                parameter["day_begin_time"] = end_time
            else:
                parameter["day_begin_time"] = time.time() - 86400
            while True:
                response = self._post(
                    "externalcontact/groupchat/statistic", data=parameter
                )
                external_behavior_list.extend(response.get("items"))
                if response.get("total") == response.get("next_offset"):
                    break
                else:
                    parameter["offset"] = response.get("next_offset")
            return external_behavior_list
        except Exception as e:
            print(e)
            return []

    def get_user_behavior_data_by_userid(
        self, userid: str, start_time: int = None, end_time: int = None
    ) -> list:
        """
         获取该userid员工「联系客户统计」数据
        https://work.weixin.qq.com/api/doc/90000/90135/92132

        :param userid: 企业微信userid标识
        :param start_time: 数据开始时间，开始时间与结束时间只传一个，默认获取传入时间当天的数据，如果两个都没有传，默认获取昨天的数据
        :param end_time: 数据结束时间
        :return: []
        """
        try:
            if start_time and end_time:
                parameter_start_time = start_time
                parameter_end_time = end_time
            elif start_time:
                parameter_start_time = start_time
                parameter_end_time = start_time
            elif end_time:
                parameter_start_time = end_time
                parameter_end_time = end_time
            else:
                # 测试时间
                # parameter_start_time = 1609224560
                # parameter_end_time = 1609224560
                yesterday = time.time() - 86400
                parameter_start_time = yesterday
                parameter_end_time = yesterday
            res = self.get_user_behavior_data(
                userid, parameter_start_time, parameter_end_time
            )
            if res.get("errcode") == 0:
                return res.get("behavior_data")
            else:
                return []
        except Exception as e:
            print(e)
            return []
