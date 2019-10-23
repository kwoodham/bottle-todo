%include('header.tpl', title='Closed Items')
%import datetime

<table>
  <tr>
    <th><b>id</b></th>
    <th><b>task</b></th>
    <th><b>project</b></th>
    <th><b>tag</b></th>
    <th><b>state</b></th>
    <th><b>date</b></th>
    <th><b>due</b></th>
  </tr>

%for row in rows:

  <tr>
  %date_due = datetime.datetime.fromisoformat(row[5]).date()
  %date_in  = datetime.datetime.fromisoformat(row[6]).date()

  <td><font>{{row[0]}}</font></td> 
  <td class="left"><font>{{row[1]}}</font></td>
  <td><font>{{row[2]}}</font></td>
  <td><font>{{row[3]}}</font></td>
  <td><font>{{row[4]}}</font></td>
  <td><font>{{date_in.strftime('%Y-%m-%d')}}</font></td>

  %if date_due.year == 2000:
    <td><font>-</font></td>
  %else:
    <td><font>{{date_due.strftime('%Y-%m-%d')}}</font></td>
  %end 
  </tr>
%end
</table>

% include('footer.tpl')
