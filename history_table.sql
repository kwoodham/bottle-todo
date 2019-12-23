select todo.id, todo.task, history.entry_date as entry_date, history.ledger 
from todo INNER JOIN history 
WHERE todo.id like history.task_id
UNION
select todo.id, todo.task, notes.entry_date as entry_date, notes.ledger
from todo INNER JOIN notes 
WHERE todo.id like notes.task_id 
ORDER by entry_date;