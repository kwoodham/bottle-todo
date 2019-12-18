% include('header.tpl', title='Edit Task %s' % no)
% import datetime

<form action="/edit/{{no}}" method="POST" enctype="multipart/form-data">

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
      <td class="left"><input type="text" name="task" value="{{old[0][1]}}" size="50" maxlength="100"></td>
      <td><select name="status">
        <option>{{old_status}}</option>
        % if old_status == 'closed':
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
  </table>

  <p></p>

  <table class="borderless">
    <tr>
      <td>
        <input type="hidden" name="task_number" value={{no}}>
        <input type="submit" name="save" value="save">
        <input type="submit" name="delete" value="delete">
        <input type="submit" name="cancel" value="back">            
        <input type="submit" name="new_note" value="new note">
        <input type="submit" name="new_file" value="new attachment">
      </td>
    </tr>
  </table>
</form>

<p></p>
  
%if old_status == 'closed':
<h3><font color="red">This task is closed - verify that you intend to edit it.</font></h3>
%end

<table>
  <tr>
    <th width=120px><b>date</b></th>
    <th width=120px><b>time</b></th>
    <th colspan=2><b>ledger</b></th>
  </tr>

  %for note in notes:
    <tr>
      %entry_date = datetime.datetime.fromisoformat(note[2])
      <td>{{entry_date.strftime('%Y-%m-%d')}}</td>
      <td>{{entry_date.strftime('%H:%M:%S')}}</td>

      <!-- make clickable notes that are links -->
      <!-- https://stackoverflow.com/questions/15551779/open-link-in-new-tab-or-window -->
      %if ( note[3][:5]=='http:' ) or ( note[3][:6]=='https:' ) or ( note[3][:5]=='file:' ) or ( note[3][:8]=='outlook:' ):
        %url_end = note[3].find(" ")
        %if url_end > 0:
          %url_text = note[3][:url_end]
          %lbl_text = note[3][(url_end+1):]
        %else:
          %url_text = note[3]
          %lbl_text = " "
        %end
        <td class="left"><a target="_blank" rel="noopener noreferrer" href="{{url_text}}">{{url_text}} </a>{{lbl_text}}</td>
      %else:
        <td class="left">{{note[3]}}</td>
      %end

      %test = note[3].split()
      %if test[0] not in ['OPENED', 'EDITED', 'CLOSED']:
        <td>
          <form action="/edit_note" method="GET">
            <input type="hidden" name="note_number" value={{note[0]}}>
            <input type="submit" name="edit_note" value="edit">
          </form>
        </td>
      %else:
        <td></td>
      %end
    </tr>
  %end
</table>

<p></p>

%if len(attachments):
<table>
  <tr>
    <th width=120px><b>date</b></th>
    <th width=120px><b>time</b></th>
    <th><b>filename</b></th>
    <th><b>description</b></th>
    <th><b>action</b></th>
  </tr>


  %for attach in attachments:
  <tr>  
    %entry_date = datetime.datetime.fromisoformat(attach[2])
    <td>{{entry_date.strftime('%Y-%m-%d')}}</td>
    <td>{{entry_date.strftime('%H:%M:%S')}}</td>
    <td class="left">{{attach[3]}}</td>
    <td class="left">{{attach[4]}}</td>
    <td>
      <form action="/edit_file" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="task_id" value={{no}}>
        <input type="hidden" name="number" value={{attach[0]}}>
        <input type="submit" name="download" value="download">
        <input type="submit" name="delete" value="delete">
      </form>
    </td>
  </tr>
  %end
</table>
%end

% include('footer.tpl')
