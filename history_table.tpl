%include('header.tpl', title='Historical Ledger')
%import datetime


<table>
  <tr>
    <th width = 10%><b>Date</b></th>
    <th width = 10%><b>Time</b></th>
    <th width = 30%><b>Text</b></th>    
    <th width = 50%><b>Ledger</b></th>
  </tr>

%for row in results:

  <tr>
    %date = datetime.datetime.fromisoformat(row[2])
    <td class="left" style="font-size:16px">{{date.strftime('%Y-%m-%d')}}</td>
    <td class="left" style="font-size:16px">{{date.strftime('%H:%M:%S')}}</td>
    <td class="left" style="font-size:16px"><a href="http://localhost:8080/view/{{row[0]}}">{{row[0]}}: {{row[1]}}</a></td> 
    <td class="left" style="font-size:16px">{{row[3]}}</td>
  </tr>

%end

 </table>

% include('footer.tpl')
