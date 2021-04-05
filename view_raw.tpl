% import datetime
%date_due = datetime.datetime.fromisoformat(old[0][6])

<pre>
number:  {{no}}
text:    {{old[0][1]}}
status:  {{old_status}}
project: {{old[0][3]}}
tag:     {{old[0][4]}}
state:   {{old[0][5]}}
%if   date_due.strftime('%Y-%m-%d') != '2000-01-01':
due:     {{date_due.strftime('%Y-%m-%d')}} 
%end
 
%for note in notes:
%entry_date = datetime.datetime.fromisoformat(note[2])
{{entry_date.strftime('%Y-%m-%d')}}/{{entry_date.strftime('%H:%M:%S')}}: {{note[3]}}
<br>---<br><br>
%end

%if len(attachments):
%for attach in attachments:
%entry_date = datetime.datetime.fromisoformat(attach[2])
{{entry_date.strftime('%Y-%m-%d')}}/{{entry_date.strftime('%H:%M:%S')}}: {{attach[3]}} ({{attach[4]}})
%end
%end
</pre>
