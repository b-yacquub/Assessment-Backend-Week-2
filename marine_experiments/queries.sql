SELECT
    e.experiment_id,
    e.subject_id,
    sp.species_name AS species,
    TO_CHAR(e.experiment_date,'yyyy-MM-dd')as experiment_date,
    et.type_name AS experiment_type,
    ROUND(
        (e.score / (et.max_score
        )) * 100, 2
    ) || '%' AS score
FROM
    experiment e
JOIN subject s USING(subject_id)
JOIN experiment_type et USING(experiment_type_id)
JOIN species sp USING(species_id)
ORDER BY e.experiment_date DESC;

(select sum(score)
from experiment
group by experiment_type_id
having e.id=experiment.id)

SELECT
    e.experiment_id,
    e.subject_id,
    sp.species_name AS species,
    TO_CHAR(e.experiment_date,'yyyy-MM-dd')as experiment_date,
    et.type_name AS experiment_type,
    ROUND(
        (e.score / (et.max_score
        )) * 100, 2
    ) || '%' AS score
FROM
    experiment e
JOIN subject s USING(subject_id)
JOIN experiment_type et USING(experiment_type_id)
JOIN species sp USING(species_id)
where (et.type_name) = 'intelligence'

SELECT
    e.experiment_id,
    e.subject_id,
    sp.species_name AS species,
    TO_CHAR(e.experiment_date,'yyyy-MM-dd')as experiment_date,
    et.type_name AS experiment_type,
    ROUND(
        (e.score / (et.max_score
        )) * 100, 2
    ) || '%' AS score
FROM
    experiment e
JOIN subject s USING(subject_id)
JOIN experiment_type et USING(experiment_type_id)
JOIN species sp USING(species_id)

SELECT
    e.experiment_id,
    e.subject_id,
    sp.species_name AS species,
    TO_CHAR(e.experiment_date,'yyyy-MM-dd')as experiment_date,
    et.type_name AS experiment_type,
    ROUND(
        (e.score / (et.max_score
        )) * 100, 2
    ) || '%' AS score
FROM
    experiment e
JOIN subject s USING(subject_id)
JOIN experiment_type et USING(experiment_type_id)
JOIN species sp USING(species_id)
where e.score::numeric / et.max_score * 100 > 90;