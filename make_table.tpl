% include('header.tpl', title='Open Items')
%import datetime
<table>
  <tr>
    <th><b>ID</b></th>
    <th><b>Task</b></th>
    <th><b>Project</b></th>
    <th><b>Tag</b></th>
    <th><b>State</b></th>
    <th><b>Date</b></th>
    <th><b>Age</b></th>
    <th><b>Due</b></th>
    <th><b>Days</b></th>
  </tr>
%for row in rows:
  %if row[4] == 'working':
    %tint = 'red'
  %elif row[4] == 'dormant':
    %tint = 'lightgrey'
  %elif row[4] == 'staging':
    %tint = 'green'
  %else:
    %tint = 'yellow'
  %end
  <tr>

  <td><font color={{tint}}>{{row[0]}}</font></td>
  <td><font color={{tint}}>{{row[1]}}</font></td>
  <td><font color={{tint}}>{{row[2]}}</font></td>
  <td><font color={{tint}}>{{row[3]}}</font></td>
  <td><font color={{tint}}>{{row[4]}}</font></td>
  <td><font color={{tint}}>{{row[5]}}</font></td>

  %old = datetime.datetime.strptime(row[5],'%Y-%m-%d')
  %new = datetime.date.today()
  %dif = new - old.date()
  <td><font color={{tint}}>{{dif.days}}</font></td>

  %due = datetime.datetime.strptime(row[6],'%Y-%m-%d')
  %if due.year == 2000:
    <td><font color={{tint}}>-</font></td>
    <td><font color={{tint}}>-</font></td>
  %else:
    <td><font color={{tint}}>{{row[6]}}</font></td>
    %dif = due.date() - datetime.date.today()
    <td><font color={{tint}}>{{dif.days}}</font></td>
  %end 

  </tr>
%end
</table>
<br>
<table>
  <tr>
    <td>
      <form action="/edit" method="get">
        <input type="text" name="number" size="5" maxlength="5">
        <input type="submit" name="edit" value="edit">
      </form>
    </td>
    <td>
      <form action="/del" method="get">
        <input type="text" name="number" size="5" maxlength="5">
        <input type="submit" name="delete" value="delete">
      </form>
    </td>
    <td>
      <form action="/new" method="get">
        <input type="submit" name="new" value="new">
      </form>
    </td>
  </tr>
</table>

% include('footer.tpl')
