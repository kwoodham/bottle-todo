% include('header.tpl', title='New Note for Task %s' % no)

<form action="/new_note/{{no}}" method="POST" enctype="multipart/form-data">
  <table>
    <tr>
      <th><b>Note</b></th>
    </tr>
    <tr>
      <td><textarea rows="5" cols="120" maxength="1000" name="note" autofocus></textarea></td>
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
