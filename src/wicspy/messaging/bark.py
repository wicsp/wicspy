"""
Bark 消息发送模块 - 通过 Bark 服务发送通知消息
"""


from typing import Dict, Optional, Any
import requests
from loguru import logger
from pydantic import BaseModel, Field

from wicspy.config import get_config


class BarkResponse(BaseModel):
    """Bark 响应模型"""
    code: int = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")


class BarkClient:
    """Bark 客户端"""
    
    def __init__(self, bark_id: Optional[str] = None):
        """
        初始化 Bark 客户端
        
        Args:
            bark_id: Bark ID，如果为 None，将从配置中获取
        """
        self.bark_id = bark_id or get_config("bark_id")
        if not self.bark_id:
            raise ValueError(
                "未设置 BARK_ID。请添加环境变量或通过配置设置，例如：'export BARK_ID=your_bark_id'"
            )
        
        self.base_url = f"https://api.day.app/{self.bark_id}"
        
    def send_message(
        self, 
        title: str, 
        content: str, 
        group: Optional[str] = None,
        sound: Optional[str] = None,
        icon: Optional[str] = None,
        url: Optional[str] = None,
        level: Optional[str] = None,
    ) -> BarkResponse:
        """
        发送 Bark 消息
        
        Args:
            title: 消息标题
            content: 消息内容
            group: 消息分组
            sound: 提示音
            icon: 图标 URL
            url: 点击消息后打开的 URL
            level: 消息级别 (active, timeSensitive, passive)
            
        Returns:
            BarkResponse: Bark 响应对象
        """
        endpoint = f"{self.base_url}/{title}/{content}"
        
        params: Dict[str, str] = {}
        if group:
            params["group"] = group
        if sound:
            params["sound"] = sound
        if icon:
            params["icon"] = icon
        if url:
            params["url"] = url
        if level:
            params["level"] = level
            
        try:
            logger.debug(f"发送 Bark 消息: {title} > {content}")
            response = requests.post(endpoint, params=params, timeout=get_config("timeout", 30))
            response.raise_for_status()
            
            logger.info(f"Bark 消息发送成功: {title}")
            
            return BarkResponse(**response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Bark 消息发送失败: {title} > {content}, 异常: {e}")
            raise


# 创建默认客户端实例
_default_client: Optional[BarkClient] = None


def get_client() -> BarkClient:
    """
    获取默认的 Bark 客户端实例
    
    Returns:
        BarkClient: Bark 客户端实例
    """
    global _default_client
    if _default_client is None:
        _default_client = BarkClient()
    return _default_client


def send_message(
    title: str, 
    content: str, 
    group: Optional[str] = None,
    sound: Optional[str] = None,
    icon: Optional[str] = None,
    url: Optional[str] = None,
    level: Optional[str] = None,
    client: Optional[BarkClient] = None,
) -> BarkResponse:
    """
    发送 Bark 消息
    
    Args:
        title: 消息标题
        content: 消息内容
        group: 消息分组
        sound: 提示音
        icon: 图标 URL
        url: 点击消息后打开的 URL
        level: 消息级别 (active, timeSensitive, passive)
        client: 自定义 Bark 客户端，如果为 None 则使用默认客户端
        
    Returns:
        BarkResponse: Bark 响应对象
    """
    if client is None:
        client = get_client()
    
    return client.send_message(
        title=title,
        content=content,
        group=group,
        sound=sound,
        icon=icon,
        url=url,
        level=level,
    ) 