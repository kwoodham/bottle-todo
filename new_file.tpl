<!DOCTYPE HTML>
<html>
<head>
<title>upload file</title>
</head>
<body>
<form action="/new_file/{{no}}" method="POST" enctype="multipart/form-data">
  <input type="file" name="upload"><br/>
  <input type="text" name="description" value="" size="50" maxlength="100">
  <input type="submit" name="submit" value="submit"><br/> 
</form>
</body>
</html>
