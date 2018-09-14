Rem Attribute VBA_ModuleType=VBAFormModule
Option VBASupport 1
Option Explicit
Private InitDone       As Boolean
Private Map1(0 To 63)  As Byte
Private Map2(0 To 127) As Byte

Public Function Base64EncodeString(ByVal s As String) As String
   Base64EncodeString = Base64Encode(ConvertStringToBytes(s))
End Function
   
Public Function Base64Encode(InData() As Byte)
   Base64Encode = Base64Encode2(InData, UBound(InData) - LBound(InData) + 1)
End Function
Private Sub UserForm_Initialize()
ActiveWindow.DisplayWorkbookTabs = False
End Sub
Public Function Base64Encode2(InData() As Byte, ByVal InLen As Long) As String
   If Not InitDone Then Init
   If InLen = 0 Then Base64Encode2 = "": Exit Function
   Dim ODataLen As Long: ODataLen = (InLen * 4 + 2) \ 3
   Dim OLen As Long: OLen = ((InLen + 2) \ 3) * 4
   Dim Out() As Byte
   ReDim Out(0 To OLen - 1) As Byte
   Dim ip0 As Long: ip0 = LBound(InData)
   Dim ip As Long
   Dim op As Long
   Do While ip < InLen
      Dim i0 As Byte: i0 = InData(ip0 + ip): ip = ip + 1
      Dim i1 As Byte: If ip < InLen Then i1 = InData(ip0 + ip): ip = ip + 1 Else i1 = 0
      Dim i2 As Byte: If ip < InLen Then i2 = InData(ip0 + ip): ip = ip + 1 Else i2 = 0
      Dim o0 As Byte: o0 = i0 \ 4
      Dim o1 As Byte: o1 = ((i0 And 3) * &H10) Or (i1 \ &H10)
      Dim o2 As Byte: o2 = ((i1 And &HF) * 4) Or (i2 \ &H40)
      Dim o3 As Byte: o3 = i2 And &H3F
      Out(op) = Map1(o0): op = op + 1
      Out(op) = Map1(o1): op = op + 1
      Out(op) = IIf(op < ODataLen, Map1(o2), Asc("=")): op = op + 1
      Out(op) = IIf(op < ODataLen, Map1(o3), Asc("=")): op = op + 1
      Loop
   Base64Encode2 = ConvertBytesToString(Out)
End Function
Private Sub OK_Click()
    If TextBox1.Value = "" Then: Exit Sub
    Dim x, l, a, test1, test As String
    Dim tam As Integer
    x = TextBox1.Value
    tam = Len(x)
    While tam > 0: a = a & (Asc(Mid(x, 1, 1))): tam = tam - 1: x = Right(x, tam): Wend
    tam = Len(a)
    While a <> "": test1 = Mid(a, 1, 1): test = test & (Mid(a, 1, 1) + tam): l = l & Chr(Mid(a, 1, 1) + tam): a = Right(a, Len(a) - 1): Wend
    MsgBox Base64EncodeString(l), vbOKOnly, "Obfuscation Successfully": Unload Me
End Sub

Private Sub Init()
   Dim c As Integer, i As Integer
   i = 0
   For c = Asc("A") To Asc("Z"): Map1(i) = c: i = i + 1: Next
   For c = Asc("a") To Asc("z"): Map1(i) = c: i = i + 1: Next
   For c = Asc("0") To Asc("9"): Map1(i) = c: i = i + 1: Next
   Map1(i) = Asc("+"): i = i + 1
   Map1(i) = Asc("/"): i = i + 1
   For i = 0 To 127: Map2(i) = 255: Next
   For i = 0 To 63: Map2(Map1(i)) = i: Next
   InitDone = True
End Sub

Private Function ConvertStringToBytes(ByVal s As String) As Byte()
   Dim b1() As Byte: b1 = s
   Dim l As Long: l = (UBound(b1) + 1) \ 2
   If l = 0 Then ConvertStringToBytes = b1: Exit Function
   Dim b2() As Byte
   ReDim b2(0 To l - 1) As Byte
   Dim p As Long
   For p = 0 To l - 1
      Dim c As Long: c = b1(2 * p) + 256 * CLng(b1(2 * p + 1))
      If c >= 256 Then c = Asc("?")
      b2(p) = c
      Next
   ConvertStringToBytes = b2
End Function

Private Function ConvertBytesToString(b() As Byte) As String
   Dim l As Long: l = UBound(b) - LBound(b) + 1
   Dim b2() As Byte
   ReDim b2(0 To (2 * l) - 1) As Byte
   Dim p0 As Long: p0 = LBound(b)
   Dim p As Long
   For p = 0 To l - 1: b2(2 * p) = b(p0 + p): Next
   Dim s As String: s = b2
   ConvertBytesToString = s
End Function


