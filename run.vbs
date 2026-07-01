Dim proj, shell, fso, chrome
proj = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
Set shell = CreateObject("WScript.Shell")
Set fso   = CreateObject("Scripting.FileSystemObject")

' Chrome 경로 탐색
Dim chromePaths(1)
chromePaths(0) = "C:\Program Files\Google\Chrome\Application\chrome.exe"
chromePaths(1) = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

chrome = ""
Dim i
For i = 0 To 1
  If fso.FileExists(chromePaths(i)) Then
    chrome = chromePaths(i)
    Exit For
  End If
Next

' 서버 실행 (숨김)
shell.Run "cmd /c cd /d """ & proj & """ && .venv\Scripts\activate.bat && uvicorn server.main:app --port 8000", 0, False

' 1초 대기 후 브라우저 열기
WScript.Sleep 1000
If chrome <> "" Then
  shell.Run """" & chrome & """ http://localhost:8000", 1, False
Else
  shell.Run "start http://localhost:8000", 0, False
End If
