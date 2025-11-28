Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener la carpeta raíz del proyecto (C:\Talent Hub)
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' === INICIAR BACKEND ===
objShell.CurrentDirectory = scriptPath

If Not fso.FileExists(scriptPath & "\main.py") Then
    MsgBox "Error: No se encontró main.py", 16, "TalentHub Error"
    WScript.Quit
End If

objShell.Run "pythonw -u main.py", 0
WScript.Sleep 3000

' === INICIAR FRONTEND ===
frontendPath = scriptPath & "\talent-hub-frontend"

If fso.FolderExists(frontendPath) Then
    objShell.CurrentDirectory = frontendPath
    
    ' Iniciar Vite sin ventana
    objShell.Run "cmd /c npm run dev", 0
    
    ' Esperar a que Vite inicie
    WScript.Sleep 6000
    
    ' Abrir el navegador en el frontend
    objShell.Run "http://localhost:5173"
Else
    MsgBox "No se encontró la carpeta talent-hub-frontend", 48, "Advertencia"
    objShell.Run "http://localhost:8000/docs"
End If

MsgBox "¡TalentHub iniciado!" & vbCrLf & vbCrLf & "Frontend: http://localhost:5173" & vbCrLf & "Backend: http://localhost:8000", 64, "TalentHub"