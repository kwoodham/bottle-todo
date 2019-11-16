% include('header.tpl', title='View Task %s' % no)
% import datetime



  <table>
    <tr>
      <th><b>text</b></th>
      <th><b>status</b></th>
      <th><b>project</b></th>
      <th><b>tag</b></th>
      <th><b>state</b></th>
      <th><b>due</b></th>
    </tr>

    <tr>
      <td width=40% class="left">{{old[0][1]}}</td>
      <td>{{old_status}}</td>
      <td>{{old[0][3]}}</td>        
      <td>{{old[0][4]}}</td>
      <td>{{old[0][5]}}</td>
      %date_due = datetime.datetime.fromisoformat(old[0][6])
      <td>{{date_due.strftime('%Y-%m-%d')}}</td>
    </tr>

    <tr>
      <td colspan=6>
        <form action="/todo" method="GET">
          <input type="submit" name="top" value="open task list">        
        </form>
        <form action="/closed" method="GET">
          <input type="submit" name="top" value="closed task list">        
        </form>
      </td>
    </tr>
  <table>


</br>
</br>
</hr>
  
<table>
  <tr>
    <th width=120px><b>date</b></th>
    <th width=120px><b>time</b></th>
    <th><b>ledger</b></th>
  </tr>

  %for note in notes:
    <tr>
      %entry_date = datetime.datetime.fromisoformat(note[2])
      <td>{{entry_date.strftime('%Y-%m-%d')}}</td>
      <td>{{entry_date.strftime('%H:%M:%S')}}</td>
      <td class="left">{{note[3]}}</td>
    </tr>
  %end
</table>

</br>
</br>
</hr>
  
<table>
  <tr>
    <th width=120px><b>date</b></th>
    <th width=120px><b>time</b></th>
    <th><b>filename</b></th>
    <th><b>description</b></th>
    <th><b>action</b></th>
  </tr>

  %for attach in attachments:
    <tr>  
      %entry_date = datetime.datetime.fromisoformat(attach[2])
      <td>{{entry_date.strftime('%Y-%m-%d')}}</td>
      <td>{{entry_date.strftime('%H:%M:%S')}}</td>
      <td class="left">{{attach[3]}}</td>
      <td class="left">{{attach[4]}}</td>
      <td>
        <form action="/edit_file" method="POST" enctype="multipart/form-data">
          <input type="hidden" name="task_id" value={{no}}>
          <input type="hidden" name="number" value={{attach[0]}}>
          <input type="submit" name="download" value="download">
        </form>
      </td>
    </tr>
  %end
</table>

% include('footer.tpl')
