% include('header.tpl', title='Open Items')
%import datetime
<table>
  <tr>
    <td><b>ID</b></td>
    <td><b>Task</b></td>
    <td><b>Project</b></td>
    <td><b>Tag</b></td>
    <td><b>State</b></td>
    <td><b>Date In</b></td>
    <td><b>Age</b></td>
  </tr>
%for row in rows:
  %if row[4] == 'working':
    %tint = 'red'
  %elif row[4] == 'dormant':
    %tint = 'lightgrey'
  %elif row[4] == 'staging':
    %tint = 'green'
  %else:
    %tint = 'black'
  %end
  <tr>
  %for col in row:
    <td><font color={{tint}}>{{col}}</font></td>
  %end

  %old = datetime.datetime.strptime(row[5],'%Y-%m-%d')
  %new = datetime.date.today()
  %dif = new - old.date()
  <td><b>{{dif.days}}</br></td>
  </tr>
%end
</table>
% include('footer.tpl')
