% include('header.tpl', title='Confirm Delete of Task %s' % no)
<form action="/del/{{no}}" method="POST">
<table>
  <tr>
    <th colspan=2>Confirm Delete</th>
  <tr>
    <td width=50% class=right>Text:</td>
    <td class=left>"{{task[0]}}"</td>
  </tr>
  <tr>
    <td colspan=2> 
      <input type="submit" name="confirm_delete" value="delete">
      <input type="submit" name="confirm_cancel" value="cancel">
    </td>
  </tr>
</table>
</form>
%include('footer.tpl')

