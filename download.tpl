%include('header.tpl', title='download')
<form action="/download" method="POST">
   <input type="text" name="record" value="">
   <input type="submit" name="submit" value="submit">
</form>
%include('footer.tpl')
