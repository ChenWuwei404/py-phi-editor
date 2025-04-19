# PyPhiEditor

Phigros 谱面编辑器。制谱就像剪视频一样简单。

Phigros chart editor made with Python and Pygame. Charting just like video editing.

## 特性 - Features

* 更符合操作逻辑的用户界面，所有人都可以快速上手
* 更简单的多线事件和音符处理
* 现代的 GUI 界面，更好的屏幕适配

---

* Simpler GUI, which almost everyone can master it at once.
* Easier muti-judge-line events and notes editor.
* Modern GUI design & better screen adaptation.

## 项目结构 - Project Structure

```mermaid
graph 

subgraph PyPhi Project

    subgraph Libaries
        subgraph Events
            pos(PyPhi.PositionPattern)
            rot(PyPhi.RotationPattern)
        end
        subgraph Notes
            note(PyPhi.NotePattern)
        end
    end

    subgraph Sence
        line(PyPhi.Judgeline) --- pos_track([PositionTrack]) --- pos_clip1(PositionClip)
        pos_clip1 --- source([Source])
        pos_clip1 --- modif([Modifier])
        pos_track --- pos_clip2(PyPhi.PositionClip)
        pos_track --- pos_clip3(. . .)

        line --- rot_track([RotationTrack]) --- rot_clip(PyPhi.RotationClip) --- source2([Source])
        rot_clip --- modif2([Modifier])

        line --- note_track([NoteTrack]) --- note_clip(PyPhi.NoteClip) --- source3([Source])
        note_clip --- modif3([Modifier])
        note_clip --- mult([MultiLineManager])

    end

    source -.- pos
    source2 -.- rot

    source3 -.- note

end
```
