select e.experiment_id,e.subject_id,sp.species_name as species
,e.experiment_date,et.type_name as experiment_type,
ROUND((e.score / 133) * 100, 2) || '%' as score
from experiment e 
join subject s using(subject_id)
join experiment_type et using(experiment_type_id)
join species sp using(species_id)
order by e.experiment_date desc;