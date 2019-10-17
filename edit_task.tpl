% include('header.tpl', title='Edit Task %s' % no)
% import datetime

<form action="/edit/{{no}}" method="get">

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
      <td><input type="text" name="task" value="{{old[0][1]}}" size="50" maxlength="100"></td>
      <td><select name="status">
        <option>{{old_status}}</option>
        % temp = old_status
        % if temp == 'closed':
        	<option>open</option>
        % else:
          <option>closed</option>
        % end
        </select>
      </td>

      <td><select name="project">
        <option>{{old[0][3]}}</option>
        %for project in projects:
          <option>{{project[0]}}</option>
        %end
      </td>        

      <td><input type="text" name="tag" value="{{old[0][4]}}" size="20" maxlength="20"></td>

      <td><select name="state">
        <option>{{old[0][5]}}</option>
        %for state in states:
          <option>{{state[0]}}</option>
        %end
        </select>
      </td>

      %date_due = datetime.datetime.fromisoformat(old[0][6])
      <td><input type="date" size="20" maxlength="20" name="date_due" value={{date_due.strftime('%Y-%m-%d')}}></td>
    </tr>

    <tr><td colspan=6><input type="submit" name="save" value="save"></td> </tr>

  <table>
</form>
% include('footer.tpl')