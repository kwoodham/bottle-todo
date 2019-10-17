% include('header.tpl', title='New Note')

<form action="/new_note/{{no}}" method="GET">
  <table>
    <tr>
      <th><b>Note</b></th>
    </tr>
    <tr>
      <td><input type="text" size="200" maxlength="5000" name="note"></td>
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