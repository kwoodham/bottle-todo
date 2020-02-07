% include('header.tpl', title='Edit Note for Task %s' % no)

<form action="/edit_note/{{no}}" method="POST" enctype="multipart/form-data">
  <h3>Place optional URL (http:, https:, outlook:, or file:) at start of the text, one per note.</h3>
  <h3>Saving a cleared note deletes it.</h3>
  <table>
    <tr>
      <th><b>Note</b></th>
    </tr>
    <tr>
      <td><textarea rows="20" cols="120" maxength="1000" 
                    name="note" value="" autofocus>{{note[0]}}</textarea>
      </td>
    </tr>
    <tr>
      <td>
        <input type="submit" name="save" value="Update">
        <input type="submit" name="cancel" value="Cancel/Return">
      </td> 
    </tr>
  </table>
</form>
% include('footer.tpl')
