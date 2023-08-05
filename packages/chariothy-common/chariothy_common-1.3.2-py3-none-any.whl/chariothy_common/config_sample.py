CONFIG = {
    'log': {
        'level': 'DEBUG',   # 与log库的level一致，包括DEBUG, INFO, ERROR
                            #   DEBUG   - Enable stdout, file, mail （如果在dest中启用）
                            #   INFO    - Enable file, mail         （如果在dest中启用）
                            #   ERROR   - Enable mail               （如果在dest中启用）
        'dest': ['stdout', 'file', 'mail'],  # 分别设置日志对象，优先级高于level设置
        'receiver': 'Henry TIAN <chariothy@gmail.com>' # 日志邮件接收者，如果为空，则使用mail.to设置
    },
    'mail': {
        'from': 'Henry TIAN <chariothy@gmail.com>',
        'to': 'Henry TIAN <chariothy@gmail.com>,Henry TIAN <6314849@qq.com>'
    },
    'smtp': {
        'host': 'smtp.google.com',
        'port': 25,
        'user': 'chariothy@gmail.com',
        'pwd': '123456'
    }
}