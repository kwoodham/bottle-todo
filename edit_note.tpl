% include('header.tpl', title='New Note')

<form action="/edit_note/{{no}}" method="POST" enctype="multipart/form-data">
  <h3>Edit note - saving a cleared note deletes it</h3>
  <table>
    <tr>
      <th><b>Note</b></th>
    </tr>
    <tr>
      <td><input type="text" size="120" maxlength="5000" name="note" value="{{note[0]}}" autofocus></td>
    </tr>
    <tr>
      <td>
        <input type="submit" name="save" value="save">
        <input type="submit" name="cancel" value="cancel">
      </td> 
    </tr>
  </table>
</form>
% include('footer.tpl')
