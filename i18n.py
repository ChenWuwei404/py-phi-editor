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
        'Copy': '拷贝',
        'Paste': '粘贴',
        'Delete': '删除',
        'Select All': '全选',

        'View': '视图',
        'Zoom In': '放大',
        'Zoom Out': '缩小',
        'Clip': '片段',
        'Note': '音符',
        'Position': '位置',
        'Rotation': '旋转',
        'Alpha': '透明度',
        'Velocity': '速度',

        'Help': '帮助',
        'About': '关于',

        'Language': '语言',
        'Chinese': '中文',
        'English': '英文',
        'Version': '版本',
        'Author': '作者',
        'License': '许可证',

        'Play': '播放',
        'Duration': '时长',
        'Volume': '音量',
        'Mute': '静音',
        'Speed': '倍速',

        'Editor': '编辑器',
        'Manager': '管理器',
        'Properties': '属性',

        'Timeline': '时间轴',
        'Track': '轨道',
        'Tracks': '轨道',
        'Pattern': '样式',
        'Patterns': '样式',
        'Clip': '片段',
        'Clips': '片段',
        'Event': '事件',
        'Events': '事件',
        'Library': '库',

        'Modifier': '修改器',
        'Multiline': '多线',
        'Source': '资源',
        'Destination': '目标',
        'Channel': '通道',
        'Mono': '单通道',
        'Stereo': '双通道',

        'Time': '时间',
        'Length': '长度',
        'Start Point': '起始点',
        'End Point': '终止点',

        'Key Point': '插值点',
        'Interpolation': '插值',
        'Linear': '线性',
        'Exp': '指数',

        'Expression': '表达式',

        'Link': '链接',
        'Unlink': '取消链接',

        'Point': '点',
        'Points': '点',
        'Judge-line': '判定线',
        'Judge-lines': '判定线',
        'Intersection': '交点',
        'Intersections': '交点',
        'Vector': '矢量',

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