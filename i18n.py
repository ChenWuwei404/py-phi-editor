languages = {
    'zh': {
        '&spliter&': '',

        'Composer': '编曲',
        'Charter': '铺面设计师',
        'Song': '曲目',
        'Arrangement': '编排',

        'File': '文件',
        'New': '新建',
        'Open': '打开',
        'Save': '保存',
        'Save As': '另存为',
        'Exit': '退出',

        'Add': '添加',
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
        'Note clip': '音符片段',
        'Position clip': '位置片段',
        'Rotation clip': '旋转片段',
        'Alpha clip': '透明度片段',
        'Speed clip': '速度片段',

        'Help': '帮助',
        'About': '关于',

        'Language': '语言',
        'Chinese': '中文',
        'English': '英文',
        'Version': '版本',
        'Author': '作者',
        'License': '许可证',

        'Play': '播放',
        'Position': '位置',
        'Duration': '时长',
        'Volume': '音量',
        'Mute': '静音',
        'Speed': '倍速',

        'Modifier': '修改器',
        'Multiline': '多线',
    }
}

global_language = 'en'

def set_language(language: str) -> None:
    global global_language
    global_language = language

def gettext(message: str) -> str:
    if global_language not in languages:
        return message
    if message in languages[global_language]:
        return languages[global_language][message]
    else:
        words = message.split()
        if len(words) == 1:
            return message
        message = languages[global_language]['&spliter&'].join(gettext(word) for word in words)
        return message