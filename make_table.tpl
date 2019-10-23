%include('header.tpl', title='Open Items')
%import datetime

%st_vec = []
%cl_vec = []
%for i in states:
    %st_vec.append(i[0])
    %cl_vec.append(i[1])
%end

<table>
  <tr>
    <th><b>id</b></th>
    <th><b>task</b></th>
    <th><b>project</b></th>
    <th><b>tag</b></th>
    <th><b>state</b></th>
    <th><b>date</b></th>
    <th><b>age</b></th>
    <th><b>due</b></th>
    <th><b>days</b></th>
  </tr>

%for row in rows:
  %tint = cl_vec[st_vec.index(row[4])]

  <tr>
  %date_due = datetime.datetime.fromisoformat(row[5]).date()
  %date_in  = datetime.datetime.fromisoformat(row[6]).date()

  <td><font color={{tint}}>{{row[0]}}</font></td> 
  <td class="left"><font color={{tint}}>{{row[1]}}</font></td>
  <td><font color={{tint}}>{{row[2]}}</font></td>
  <td><font color={{tint}}>{{row[3]}}</font></td>
  <td><font color={{tint}}>{{row[4]}}</font></td>
  <td><font color={{tint}}>{{date_in.strftime('%Y-%m-%d')}}</font></td>


  %dif = datetime.date.today() - date_in
  <td><font color={{tint}}>{{dif.days}}</font></td>

  %if date_due.year == 2000:
    <td><font color={{tint}}>-</font></td>
    <td><font color={{tint}}>-</font></td>
  %else:
    <td><font color={{tint}}>{{date_due.strftime('%Y-%m-%d')}}</font></td>
    %dif = date_due - datetime.date.today()
    <td><font color={{tint}}>{{dif.days}}</font></td>
  %end 

  </tr>
%end
</table>
<br>
<table>
  <tr>
    <td colspan=2>
      <form action="/modify" method="get">
        <input type="text" name="number" size="5" maxlength="5">
        <input type="submit" name="edit" value="edit">
        <input type="submit" name="delete" value="delete">
      </form>
    </td>
    <td colspan=5>
      <form action="/filter" method="get">
        <input type="text" name="project" size="12" maxlength="20">
        <input type="text" name="tag" size="12" maxlength="20">
        <input type="text" name="state" size="12" maxlength="20">
        <input type="submit" name="filter" value="filter">
      </form>
    </td>
    <td colspan=2>
      <form action="/new" method="get">
        <input type="submit" name="new" value="new" autofocus>
      </form>
    </td>
  </tr>
</table>

% include('footer.tpl')
