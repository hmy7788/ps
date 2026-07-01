Dim fso, shell, shortcut, proj, desktop

Set fso   = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

proj    = fso.GetParentFolderName(WScript.ScriptFullName)
desktop = shell.SpecialFolders("Desktop")

Set shortcut = shell.CreateShortcut(desktop & "\PS Platform.lnk")
shortcut.TargetPath       = "wscript.exe"
shortcut.Arguments        = """" & proj & "\run.vbs"""
shortcut.WorkingDirectory = proj
shortcut.Description      = "PS Platform 서버 시작"
shortcut.IconLocation     = proj & "\PS Platform Icon.ico, 0"
shortcut.Save

MsgBox "바탕화면에 'PS Platform' 바로가기가 생성됐습니다!", vbInformation, "완료"
