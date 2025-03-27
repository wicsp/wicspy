import argparse
from wicspy.messaging.bark import send_message
from loguru import logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="发送 Bark 通知消息")
    parser.add_argument("title", help="消息标题")
    parser.add_argument("content", help="消息内容")
    parser.add_argument("--group", "-g", help="消息分组")
    parser.add_argument("--sound", "-s", help="提示音")
    parser.add_argument("--icon", "-i", help="图标 URL")
    parser.add_argument("--url", "-u", help="点击消息后打开的 URL")
    parser.add_argument(
        "--level", 
        "-l",
        choices=["active", "timeSensitive", "passive"],
        help="消息级别"
    )
    return parser


def bark():
    """Bark 命令行工具入口点"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        response = send_message(
            title=args.title,
            content=args.content,
            group=args.group,
            sound=args.sound,
            icon=args.icon,
            url=args.url,
            level=args.level,
        )
        if response.code == 200:
            logger.info("消息发送成功")
        else:
            logger.error(f"消息发送失败: {response.message}")
    except Exception as e:
        logger.error(f"发送消息时发生错误: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    bark()
