% include('header.tpl', title='New Task')
<p>Add a new task to the ToDo list:</p>
<form action="/new" method="GET">
  <table>
    <tr>
      <th><b>text</b></th>
      <th><b>project</b></th>
      <th><b>tag</b></th>
      <th><b>state</b></th>
      <th><b>due</b></th>
    </tr>
    <tr>
      <td><input type="text" size="50" maxlength="50" name="task"></td>
      <td><input type="text" size="20" maxlength="20" name="project"></td>
      <td><input type="text" size="20" maxlength="20" name="tag"></td>
      <td><select name="state">
        <option>dormant</option>
        <option>staging</option>
        <option>working</option>
        <option>waiting</option>
        </select>
      </td>
      <td><input type="date" size="20" maxlength="20" name="date_due" value='2000-01-01'></td>
    </tr>
    <tr><td colspan=5><input type="submit" name="save" value="save"></td> </tr>
  </table>
</form>
% include('footer.tpl')