% include('header.tpl', title='View Task %s' % no)
% import datetime



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
    <td width=40% class="left">{{old[0][1]}}</td>
    <td>{{old_status}}</td>
    <td>{{old[0][3]}}</td>        
    <td>{{old[0][4]}}</td>
    <td>{{old[0][5]}}</td>
    %date_due = datetime.datetime.fromisoformat(old[0][6])
    <td>{{date_due.strftime('%Y-%m-%d')}}</td>
  </tr>
</table>

<p></p>

<table class="borderless">
  <tr>
    <td width=50% class="right">
      <form action="/todo" method="GET">
        <input type="submit" name="top" value="open task list">        
      </form>
    </td>
    <td class="left">
      <form action="/closed" method="GET">
        <input type="submit" name="top" value="closed task list">        
      </form>
    </td>
  </tr>
</table>

<p></p>

<h3>Note: Browser security may require file URL cut/paste into new tab</h3>

<table>
  <tr>
    <th width=120px><b>date</b></th>
    <th width=120px><b>time</b></th>
    <th><b>ledger</b></th>
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
        </form>
      </td>
    </tr>
  %end
</table>
%end

% include('footer.tpl')
