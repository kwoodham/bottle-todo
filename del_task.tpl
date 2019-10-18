%#template for the form for a new task
<p>Task {{no}} text is: {{task[0]}}</p>
<br>
<form action="/del/{{no}}" method="GET">
  <input type="submit" name="delete" value="delete">
</form>
