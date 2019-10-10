%#template for the form for a new task
<p>Add a new task to the ToDo list:</p>
<form action="/new" method="GET">
  <input type="text" size="100" maxlength="100" name="task">
  <input type="text" size="20" maxlength="20" name="project">
  <input type="text" size="20" maxlength="20" name="tag">
  <select name="state">
    <option>dormant</option>
    <option>staging</option>
    <option>working</option>
    <option>waiting</option>
  </select>
  <br>
  <input type="submit" name="save" value="save">
</form>
