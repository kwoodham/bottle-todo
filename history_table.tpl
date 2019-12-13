%include('header.tpl', title='Historical Ledger')
%import datetime


<table>
  <tr>
    <th width = 10%><b>Date</b></th>
    <th width = 10%><b>Time</b></th>
    <th width = 5%><b>Task</b></th>
    <th width = 25%><b>Text</b></th>    
    <th width = 50%><b>Ledger</b></th>
  </tr>

%for row in results:

  <tr>
    %date = datetime.datetime.fromisoformat(row[2])
    <td class="left">{{date.strftime('%Y-%m-%d')}}</td>
    <td class="left">{{date.strftime('%H:%M:%S')}}</td>
    <td class="left">{{row[0]}}</td> 
    <td class="left">{{row[1]}}</td>
    <td class="left">{{row[3]}}</td>
  </tr>

%end

 </table>

% include('footer.tpl')
