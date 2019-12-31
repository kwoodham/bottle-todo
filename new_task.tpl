% include('header.tpl', title='New Task')
<h3>new task:</h3>
<form action="/new" method="POST" enctype="multipart/form-data">
  <table>
    <tr>
      <th><b>text</b></th>
      <th><b>project</b></th>
      <th><b>tag</b></th>
      <th><b>state</b></th>
      <th><b>due</b></th>
    </tr>
    <tr>
      <td><input type="text" size="40" maxlength="100" name="task" autofocus></td>

      <td><select name="project">
        %for project in projects:
          <option>{{project[0]}}</option>
        %end
        </select>
      </td>

      <td><input type="text" size="15" maxlength="20" name="tag"></td>

      <td><select name="state">
        %for state in states:
          <option>{{state[0]}}</option>
        %end
        </select>
      </td>

      <td><input type="date" size="15" maxlength="20" name="date_due" value='2000-01-01'></td>

    </tr>
      <tr><td colspan=5>
        <input type="submit" name="save" value="save">
        <input type="submit" name="cancel" value="cancel">
      </td> 
    </tr>
  </table>
</form>
% include('footer.tpl')
