# -*- coding: utf-8 -*-
# Author: shenglong
# Date: 2021/1/12
import requests

from flexiv_consul_service.src.base_service import ConsulBaseService


def register_service(ip, port, service_list):
    if not isinstance(service_list, list):
        raise TypeError("service list must be list params")
    if not service_list:
        raise Exception("service_list not allow empty")

    consul_client = ConsulBaseService()
    for service in service_list:
        service_id = service + ip + ':' + str(port)
        consul_client.register(service, service_id=service_id, address=ip, port=port, tags=['master'])


def get_service_info(service_name: str, token: str, **kwargs):
    if not service_name:
        raise Exception("not allow service empty")
    if not token:
        raise Exception("not allow token empty")

    consul_client = ConsulBaseService()
    ip, port = consul_client.get_service(service_name)

    headers = {"Authorization": f"jwt {token}"}
    if kwargs:
        service_res = requests.get(f"http://{ip}:{port}/{service_name}",params=kwargs, headers=headers).text
    else:
        service_res = requests.get(f"http://{ip}:{port}/{service_name}", headers=headers).text
    return service_res.get("data")













