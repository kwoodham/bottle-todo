%include('header.tpl', title='upload for task {{no}}')
<form action="/new_file/{{no}}" method="POST" enctype="multipart/form-data">
<table>
  <tr>
    <th colspan=2>Attach File</th>
  <tr>
    <td width=50% class=right>File:</td>
    <td class=left><input type="file" name="upload" class="inputfile"> </td>
  </tr>
  <tr>
    <td class=right>Description:</td>
    <td class=left> <input type="text" name="description" value="" size="50" maxlength="100"> </td>
  </tr>
  <tr>
    <td colspan=2> 
      <input type="submit" name="submit" value="submit">
      <input type="submit" name="cancel" value="cancel"> 
    </td>
  </tr>
</table>
</form>
%include('footer.tpl')
