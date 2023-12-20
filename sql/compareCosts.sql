select
	a.filename as fname,
	(a.grandtotal - b.grandtotal) as new_total
from
	denials a,
    denials b
where
	a.denialid < 11
	and b.denialid > 10
    and a.denialid = b.denialid
order by 
	a.denialid asc