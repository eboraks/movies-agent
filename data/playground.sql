SELECT m.title, pc.name AS production_country 
FROM movie AS m 
INNER JOIN movie_production_country_link AS mgl ON m.id = mgl.movie_id
INNER JOIN production_country AS pc ON mgl.country_id = pc.id
WHERE m.title like '%2 Guns%'