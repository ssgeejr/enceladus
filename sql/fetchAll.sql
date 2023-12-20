select
a.*,
b.*
from
denials a,
adjustments b
where 
a.denialid <11
and b.denialid > 10
and 
a.denialid = b.denialid
order by a.grandtotal desc