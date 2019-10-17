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

    <tr>
      <td colspan=6>
        <input type="hidden" name="number" value={{no}}>
        <input type="submit" name="save" value="save">
        <input type="submit" name="cancel" value="cancel">        
        <input type="submit" name="new_note" value="new note">
      </td>
    </tr>

  <table>
</form>

</br>
</br>
</hr>
  
<table>
  <tr>
    <th><b>date</b></th>
    <th><b>time</b></th>
    <th colspan=2><b>ledger</b></th>
  </tr>

  %for note in notes:
    <tr>
      %entry_date = datetime.datetime.fromisoformat(note[2])
      <td>{{entry_date.strftime('%Y-%m-%d')}}</td>
      <td>{{entry_date.strftime('%H:%M:%S')}}</td>
      <td class="left">{{note[3]}}</td>

      %if note[3] not in ['OPENED', 'EDITED', 'CLOSED']:
        <td>
          <form action="/edit" method="get">
            <input type="hidden" name="number" value={{note[0]}}>
            <input type="submit" name="modify" value="M">
            <input type="submit" name="delete" value="D">
          </form>
        </td>
      %else:
        <td></td>
      %end
    </tr>
  %end
</table>



% include('footer.tpl')