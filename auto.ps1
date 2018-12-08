Get-ChildItem data\*.jpg | ForEach-Object{
  python.exe .\wbKiridashi.py $_.fullname 
}