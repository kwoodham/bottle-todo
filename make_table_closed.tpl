%include('header.tpl', title='Closed Items')
%import datetime

<table>
  <tr>
    <th><b>id</b></th>
    <th><b>task</b></th>
    <th><b>project</b></th>
    <th><b>tag</b></th>
    <th><b>state</b></th>
    <th><b>closed</b></th>
  </tr>

%for row in rows:

  <tr>
    <td>{{row[0]}}</td> 
    <td class="left"><a href='/view/{{row[0]}}'><font color='lightgrey'>{{row[1]}}</font></a></td>
    <td>{{row[2]}}</td>
    <td>{{row[3]}}</td>
    <td>{{row[4]}}</td>
    %date_in  = datetime.datetime.fromisoformat(row[6]).date()
    <td>{{date_in.strftime('%Y-%m-%d')}}</td>
  </tr>
%end
</table>

%include('footer.tpl')
