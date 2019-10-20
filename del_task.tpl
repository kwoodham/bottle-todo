% include('header.tpl', title='Confirm Delete')
<p>Task {{no}} text is: {{task[0]}}</p>
<br>
<form action="/del/{{no}}" method="GET">
  <input type="submit" name="confirm_delete" value="delete">
  <input type="submit" name="confirm_cancel" value="cancel">
</form>
% include('footer.tpl')
