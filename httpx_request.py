import httpx
from typing import Dict, Any

"""
xjbot 请求框架
"""


class AsyncHttpClient:
    def __init__(self, max_connections: int = 20):
        self.client = httpx.AsyncClient(limits=httpx.Limits(max_connections=max_connections))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def get(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        """
        异步发送GET请求。
        """
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.TimeoutException as e:
            raise Exception("请求超时") from e
        except httpx.RequestError as e:
            raise Exception(f"网络请求错误: {e}") from e
        except httpx.HTTPStatusError as e:
            raise Exception(f"服务器返回错误: {e.response.status_code} - {e.response.text}") from e

    async def post(self, url: str, json: Dict[str, Any] = None, data: Dict[str, Any] = None, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        """
        异步发送POST请求。
        """
        try:
            response = await self.client.post(url, json=json, data=data, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.TimeoutException as e:
            raise Exception("请求超时") from e
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            raise Exception(f"请求错误: {str(e)}") from e

    async def close(self):
        await self.client.aclose()


class HttpClient:
    def __init__(self):
        """
        初始化HttpClient实例。
        """
        self.client = httpx.Client()

    def get(self, url, params=None, headers=None):
        """
        发送GET请求。
        :param url: 完整的请求URL
        :param params: 查询参数字典
        :param headers: 请求头字典
        :return: httpx.Response对象或None（如果发生错误）
        """
        try:
            response = self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            print(f"网络请求错误: {e}")
        except httpx.HTTPStatusError as e:
            print(f"服务器返回错误: {e.response.text}")
        return None

    def post(self, url, json=None, data=None, params=None, headers=None):
        """
        发送POST请求。
        :param url: 完整的请求URL
        :param json: JSON格式的数据
        :param data: 表单数据
        :param params: 查询参数字典
        :param headers: 请求头字典
        :return: httpx.Response对象或None（如果发生错误）
        """
        try:
            response = self.client.post(url, json=json, data=data, params=params, headers=headers)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            print(f"网络请求错误: {e}")
        except httpx.HTTPStatusError as e:
            print(f"服务器返回错误: {e.response.text}")
        return None

    def close(self):
        self.client.close()
