<p>Edit the task with ID = {{no}}</p>
<form action="/edit/{{no}}" method="get">
  <input type="text" name="task" value="{{old[0][1]}}" size="100" maxlength="100">
  <select name="status">
    <option>{{old_status}}</option>
    % temp = old_status
    % if temp == 'closed':
    	<option>open</option>
    % else:
	<option>closed</option>
    % end
  </select>
  <input type="text" name="project" value="{{old[0][3]}}" size="20" maxlength="20">
  <input type="text" name="tag" value="{{old[0][4]}}" size="20" maxlength="20">

  <select name="state">
    <option>{{old[0][5]}}</option>
    % temp = old
    % if not temp[0][5] == 'dormant':
    	<option>dormant</option>
    % end
    % if not temp[0][5] == 'working':
    	<option>working</option>
    % end
    % if not temp[0][5] == 'waiting':
    	<option>waiting</option>
    % end
  </select>
  <br>
  <input type="submit" name="save" value="save">
</form>
