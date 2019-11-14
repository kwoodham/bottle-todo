<!DOCTYPE HTML>
<html>
<head>
<title>upload file</title>
</head>
<body>
<table border=0>
  <tr><td><b>File Name:</b></td><td>{{name}}</td></tr>
  <tr><td><b>File Type:</b></td><td>{{filetype}}</td></tr>
  <tr><td><b>File Size:</b></td><td>{{size}}</td></tr>
</table>

<form action='/upload' method='GET'>
  <input type='submit' name='Next File' value='next-file'>
</form>

</body>
</html>


