% include('header.tpl', title='Confirm Delete of File')
<form action="/del_file" method="POST">
<input type="hidden" name="task_id"  value={{task_id}}>
<input type="hidden" name="file_id"  value={{file_id}}>
<input type="hidden" name="filename" value={{filename}}>
<input type="hidden" name="isoname"  value={{isoname}}>
<input type="hidden" name="filetype" value={{filetype}}>
<table>
  <tr>
    <th colspan=2>Confirm Delete</th>
  <tr>
    <td width=50% class=right>Filename:</td>
    <td class=left>"{{filename}}"</td>
  </tr>
  <tr>
    <td width=50% class=right>Filetype:</td>
    <td class=left>"{{filetype}}"</td>
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
