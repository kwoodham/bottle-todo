%include('header.tpl', title='Open Items')
%import datetime

%st_vec = []
%cl_vec = []
%for i in states:
    %st_vec.append(i[0])
    %cl_vec.append(i[1])
%end

%item_count = len(rows)
<table>
  <tr>
    <th><b>id</b></th>
    <th><b>task ({{item_count}})</b></th>
    <th><b>project</b></th>
    <th><b>tag</b></th>
    <th><b>state</b></th>
    <th><b>age</b></th>
    <th><b>due</b></th>
    <th><b>days</b></th>
  </tr>

  <tr>

    <form action="/filter" method="POST" enctype="multipart/form-data">
      %table_p = []
      %table_t = []
      %table_s = []
      %for row in rows:
        %table_p.append(row[2])
        %table_t.append(row[3])
        %table_s.append(row[4])
      %end

      %table_p = list(set(table_p)) # generate a set of unique values
      %table_t = list(set(table_t))
      %table_s = list(set(table_s))

      %table_p.sort()
      %table_t.sort()
      %table_s.sort()

      <td></td>

      <td class="left">
        <input type="text" size="40" maxlength="100" name="task_string", value="search text">
      </td>

      <td><select name="project">
        <option>all</option>
        %for p in table_p:
          <option>{{p}}</option>
        %end
        </select>
      </td>

      <td><select name="tag">
        <option>all</option>
        %for t in table_t:
          <option>{{t}}</option>
        %end
        </select>
      </td>

      <td><select name="state">
        <option>all</option>
        <option>!dormant</option>
        %for s in table_s:
          <option>{{s}}</option>
        %end
        </select>
      </td>

      <td class="left" colspan=3><input type="submit" name="filter" value="?"></td>

    </form>

  </tr>

  <tr><td colspan=8></td></tr>

%for row in rows:
  %tint = cl_vec[st_vec.index(row[4])]

  <tr>
  %date_due = datetime.datetime.fromisoformat(row[5]).date()
  %date_in  = datetime.datetime.fromisoformat(row[6]).date()

  <td><font color={{tint}}>{{row[0]}}</font></td> 
  <td class="left"><a href='/edit/{{row[0]}}'><font color={{tint}}>{{row[1]}}</font></a></td>
  <td><font color={{tint}}>{{row[2]}}</font></td>
  <td><font color={{tint}}>{{row[3]}}</font></td>
  <td><font color={{tint}}>{{row[4]}}</font></td>

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

  <tr><td colspan=8></td></tr>

  <form action="/new" method="POST" enctype="multipart/form-data">
    <tr>
      <td></td>

      <td class="left"><input type="text" size="40" maxlength="100" name="task" autofocus></td>

      <td><select name="project">
        <option></option>
        %for project in projects:
          <option>{{project[0]}}</option>
        %end
        </select>
      </td>

      <td><input type="text" size="15" maxlength="20" name="tag"></td>

      <td><select name="state">
        <option></option>
        %for state in states:
          <option>{{state[0]}}</option>
        %end
        </select>
      </td>

      <td><input type="submit" name="save" value="+"></td>
      <td><input type="hidden" size="15" maxlength="20" name="date_due" value='2000-01-01'></td>
      <td></td> 
    </tr>
  </form>

</table>

% include('footer.tpl')
