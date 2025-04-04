languages = {
    'zh': {
        'File': '文件',
        'New': '新建',
        'Open': '打开',
        'Save': '保存',
        'Save As': '另存为',
        'Exit': '退出',
        'Edit': '编辑',
        'Undo': '撤销',
        'Redo': '重做',
        'Cut': '剪切',
        'Copy': '复制',
        'Paste': '粘贴',
        'Delete': '删除',
        'Select All': '全选',
        'View': '视图',
        'Zoom In': '放大',
        'Zoom Out': '缩小',
        'Help': '帮助',
        'About': '关于',
        'Language': '语言',
        'Chinese': '中文',
        'English': '英文',
        'Version': '版本',
        'Author': '作者',
        'License': '许可证',
        'Play': '播放',
    }
}

global_language = 'en'

def set_language(language: str) -> None:
    global global_language
    global_language = language

def gettext(message: str) -> str:
    try:
        return languages[global_language][message]
    except KeyError:
        return message